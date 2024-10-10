from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Document, Video, Enrollment, ReadingMaterial, Completion, CourseMaterial, Session
from .forms import CourseForm, DocumentForm, VideoForm, EnrollmentForm, CourseSearchForm, SessionForm
from module_group.models import ModuleGroup
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
import os
from django.http import FileResponse,Http404
from django.utils.text import slugify
from django.urls import reverse
from feedback.models import CourseFeedback
from .forms import ExcelImportForm
from django.http import HttpResponse
import openpyxl
import pandas as pd
from user.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime
import base64
from itertools import zip_longest
import numpy as np


def export_course(request):
    # Create a workbook and add a worksheet
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=lms_course.xlsx'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Course'

    # Define the columns
    columns = [
        'name',
        'course_code',
        'description',
        'creator',
        'instructor',
        'published',
        'prerequisites'
    ]
    worksheet.append(columns)

    # Fetch all courses and write to the Excel file
    for course in Course.objects.all():
        prerequisites_list = ', '.join([prerequisite.name for prerequisite in course.prerequisites.all()])
        worksheet.append([
            course.name,
            course.course_code,
            course.description,
            course.creator.username if course.creator else 'N/A',  # Use username or other identifier
            course.instructor.username if course.instructor else 'N/A',  # Use username or other identifier
            course.published,
            prerequisites_list or 'N/A'  # Show N/A if there are no prerequisites
        ])

    workbook.save(response)
    return response

def to_none_if_nan(value):
    """Convert value to None if it is NaN."""
    if isinstance(value, float) and np.isnan(value):
        return None
    return value

def import_courses(request):
    if request.method == 'POST':
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(uploaded_file)
                course_imported = 0
                course_updated = 0

                for index, row in df.iterrows():
                    name = row['name']
                    course_code = row['course_code']
                    description = row['description']
                    creator_username = to_none_if_nan(row.get('creator'))
                    instructor_username = to_none_if_nan(row.get('instructor'))
                    prerequisites = to_none_if_nan(row.get('prerequisites'))

                    print(f"Processing row: {name}")
                    # Fetch User instances
                    creator = None
                    if creator_username:
                        try:
                            creator = User.objects.get(username=creator_username)
                        except User.DoesNotExist:
                            messages.warning(request,
                                             f"Creator '{creator_username}' does not exist. Skipping course '{name}'.")
                            continue

                    instructor = None
                    if instructor_username:
                        try:
                            instructor = User.objects.get(username=instructor_username)
                        except User.DoesNotExist:
                            messages.warning(request,
                                             f"Instructor '{instructor_username}' does not exist. Skipping course '{name}'.")
                            continue

                    # Get or create the course
                    course, created = Course.objects.get_or_create(
                        name=name,
                        defaults={
                            'course_code': course_code,
                            'description': description,
                            'creator': creator,
                            'instructor': instructor,
                        }
                    )

                    if created:
                        course_imported += 1
                        print(f"Course '{name}' created")
                    else:
                        course_updated += 1
                        print(f"Course '{name}' already exists and was not created")
                    # Handle prerequisites
                    if prerequisites:
                        prerequisite_names = [prerequisite.strip() for prerequisite in prerequisites.split(',')]
                        # Clear existing prerequisites
                        course.prerequisites.clear()
                        # Add new prerequisites
                        for prerequisite_name in prerequisite_names:
                            try:
                                prerequisite = Course.objects.get(name=prerequisite_name)
                                course.prerequisites.add(prerequisite)
                                print(f"Added prerequisite '{prerequisite_name}' to course '{name}'.")
                            except Course.DoesNotExist:
                                print(f"Prerequisite '{prerequisite_name}' does not exist for course '{name}'.")

                messages.success(request,
                                 f"{course_imported} courses imported successfully! {course_updated} courses already existed.")
            except Exception as e:
                messages.error(request, f"An error occurred during import: {e}")
                print(f"Error during import: {e}")

            return redirect('course:course_list')
    else:
        form = ExcelImportForm()

    return render(request, 'course_list.html', {'form': form})


@login_required
def course_enroll(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)

        if form.is_valid():
            enrollment = form.save(commit=False)

            # Fetch prerequisite courses from the Course model
            prerequisite_courses = course.prerequisites.all()

            # Check if the user is enrolled in all prerequisite courses
            if prerequisite_courses.exists():
                enrolled_courses = Enrollment.objects.filter(
                    student=request.user,
                    course__in=prerequisite_courses
                ).values_list('course', flat=True)

                # Ensure all prerequisites are met
                if not all(prereq.id in enrolled_courses for prereq in prerequisite_courses):
                    form.add_error(None, 'You do not meet the prerequisites for this course.')
                    return render(request, 'course_enroll.html', {'form': form, 'course': course})

            # If prerequisites are met, save the enrollment
            enrollment.student = request.user
            enrollment.course = course
            enrollment.save()
            return redirect('course:course_list')
    else:
        form = EnrollmentForm()

    return render(request, 'course_enroll.html', {'form': form, 'course': course})


@login_required
def course_unenroll(request, pk):
    course = get_object_or_404(Course, pk=pk)
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
        enrollment.delete()
    except Enrollment.DoesNotExist:
        pass  # Có thể thêm thông báo lỗi nếu cần

    return redirect('course:course_list')


def course_list(request):
    if request.user.is_superuser:
        # Superuser can see all courses
        courses = Course.objects.all()
    elif Course.objects.filter(instructor=request.user).exists():
        # Instructors can see all courses they are teaching, published or not
        courses = Course.objects.filter(
            Q(published=True) | Q(instructor=request.user)
        )
    else:
        courses = Course.objects.filter(published=True)  # Other users see only published courses

    module_groups = ModuleGroup.objects.all()
    enrollments = Enrollment.objects.filter(student=request.user)
    enrolled_courses = {enrollment.course.id for enrollment in enrollments}

    # Calculate completion percentage for each course
    for course in courses:
        course.completion_percent = course.get_completion_percent(request.user)

    # Pagination
    paginator = Paginator(courses, 10)  # Show 10 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'course_list.html', {
        'module_groups': module_groups,
        'page_obj': page_obj,  # Pagination object for template
        'courses': page_obj,  # Consistent with template expectations
        'enrolled_courses': enrolled_courses,  # To show enrolled status
    })

def course_add(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST)

        if course_form.is_valid():
            # Save the course
            course = course_form.save(commit=False)
            course.creator = request.user
            course.save()

            # Handle prerequisite courses (optional)
            prerequisite_ids = request.POST.getlist('prerequisite_courses[]')
            for prerequisite_id in prerequisite_ids:
                if prerequisite_id:
                    prerequisite_course = Course.objects.get(id=prerequisite_id)
                    course.prerequisites.add(prerequisite_course)

            # Create sessions for the course directly
            session_name = request.POST.get('session_name')
            session_quantity = int(request.POST.get('session_quantity', 0))
            if session_name and session_quantity > 0:
                for i in range(1, session_quantity + 1):
                    session = Session(
                        course=course,
                        name=f"{session_name}{i}",
                        order=i
                    )
                    session.save()

            messages.success(request, 'course and sessions created successfully.')
            return redirect('course:course_list')
        else:
            messages.error(request, 'There was an error creating the course. Please check the form.')

    else:
        course_form = CourseForm()
        session_form = SessionForm()

    all_courses = Course.objects.all()

    return render(request, 'course_form.html', {
        'course_form': course_form,
        'session_form': session_form,
        'all_courses': all_courses,
    })

# course/views.py
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    all_courses = Course.objects.exclude(id=course.id)

    if request.method == 'POST':
        course_form = CourseForm(request.POST, instance=course)

        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.creator = request.user
            course.save()

            # Handle prerequisite deletion
            current_prerequisites = list(course.prerequisites.all())
            for prereq in current_prerequisites:
                if request.POST.get(f'delete_prerequisite_{prereq.id}'):
                    course.prerequisites.remove(prereq)

            # Handle adding new prerequisites
            prerequisite_ids = request.POST.getlist('prerequisite_courses')
            for prerequisite_id in prerequisite_ids:
                if prerequisite_id:
                    prerequisite_course = Course.objects.get(id=prerequisite_id)
                    course.prerequisites.add(prerequisite_course)

            # Handle sessions update
            session_ids = request.POST.getlist('session_ids')
            session_names = request.POST.getlist('session_names')
            for session_id, session_name in zip(session_ids, session_names):
                session = Session.objects.get(id=session_id)
                session.name = session_name
                session.save()

            # Handle adding new sessions
            new_session_names = request.POST.getlist('new_session_names')
            for session_name in new_session_names:
                if session_name:
                    Session.objects.create(course=course, name=session_name, order=course.sessions.count() + 1)

            # Handle session deletion
            delete_session_ids = request.POST.getlist('delete_session_ids')
            for session_id in delete_session_ids:
                Session.objects.filter(id=session_id).delete()

            messages.success(request, 'course updated successfully.')
            return redirect('course:course_list')
        else:
            messages.error(request, 'There was an error updating the course. Please check the form.')

    else:
        course_form = CourseForm(instance=course)
        prerequisites = course.prerequisites.all()
        sessions = course.sessions.all()

    return render(request, 'edit_form.html', {
        'course_form': course_form,
        'course': course,
        'prerequisites': prerequisites,
        'all_courses': all_courses,
        'sessions': sessions,  # Pass sessions to template
    })

def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course:course_list')
    return render(request, 'course_confirm_delete.html', {'course': course})


def resource_library(request):
    documents = Document.objects.all()
    videos = Video.objects.all()
    courses = Course.objects.all()

    selected_course_id = request.GET.get('course')
    if selected_course_id:
        documents = documents.filter(course_id=selected_course_id)
        videos = videos.filter(course_id=selected_course_id)

    return render(request, 'resource_library.html', {
        'documents': documents,
        'videos': videos,
        'courses': courses,
        'selected_course_id': selected_course_id,
    })

@login_required
def course_detail(request, pk):
    # Get the course based on the primary key (pk)
    course = get_object_or_404(Course, pk=pk)

    # Get related documents and videos
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    users_enrolled_count = Enrollment.objects.filter(course=course).count()

    # Get all feedback related to the course
    feedbacks = CourseFeedback.objects.filter(course=course)

    # Calculate the course's average rating
    if feedbacks.exists():
        total_rating = sum(feedback.average_rating() for feedback in feedbacks)
        course_average_rating = total_rating / feedbacks.count()
    else:
        course_average_rating = None  # No feedback yet

    # Get prerequisite courses directly from the course's `prerequisites` column
    prerequisites = course.prerequisites.all()

    sessions = Session.objects.filter(course=course)

    context = {
        'course': course,
        'prerequisites': prerequisites,  # Pass prerequisites from the course model
        'is_enrolled': is_enrolled,
        'users_enrolled_count': users_enrolled_count,
        'course_average_rating': course_average_rating,
        'feedbacks': feedbacks,  # Pass feedbacks to the template
        'sessions': sessions,
    }

    return render(request, 'course_detail.html', context)


def file_download(request, file_type, file_id):
    if file_type == 'document':
        file_obj = get_object_or_404(Document, id=file_id)
        file_path = file_obj.doc_file.path
        file_name = file_obj.doc_title
    elif file_type == 'video':
        file_obj = get_object_or_404(Video, id=file_id)
        file_path = file_obj.vid_file.path
        file_name = file_obj.vid_title
    else:
        raise Http404("File not found")

    file_extension = os.path.splitext(file_path)[1].lower()
    previewable_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.ogg']

    if file_extension in previewable_extensions:
        # For previewable files, open them in the browser
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'inline; filename="{slugify(file_name)}{file_extension}"'
    else:
        # For non-previewable files, force download
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{slugify(file_name)}{file_extension}"'

    return response


def users_enrolled(request, pk):
    # Lấy môn học dựa trên khóa chính (primary key)
    course = get_object_or_404(Course, pk=pk)

    # Lấy danh sách người dùng đã đăng ký môn học
    enrolled_users = Enrollment.objects.filter(course=course).select_related('student')

    return render(request, 'users_course_enrolled.html', {
        'course': course,
        'enrolled_users': enrolled_users,
    })

def course_search(request):
    form = CourseSearchForm(request.GET or None)
    query = request.GET.get('query', '')
    courses = Course.objects.all()

    if query:
        courses = courses.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(course_code__icontains=query))

    # Add pagination for search results
    paginator = Paginator(courses, 10)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,  # For paginated results
        'courses': page_obj,  # Pass the paginated courses as 'courses' for template consistency
    }
    return render(request, 'course_list.html', context)

@login_required
def reorder_course_materials(request, pk, session_id):
    # Fetch the course
    course = get_object_or_404(Course, pk=pk)

    # Fetch all sessions related to the course
    sessions = Session.objects.filter(course=course)

    # Fetch materials for the selected session, defaulting to the first session
    selected_session_id = request.POST.get('session_id') or session_id
    session = get_object_or_404(Session, id=selected_session_id)
    materials = CourseMaterial.objects.filter(session=session).order_by('order')

    if request.method == 'POST':
        # Check if the request is for reordering materials
        if 'order' in request.POST:
            for material in materials:
                new_order = request.POST.get(f'order_{material.id}')
                if new_order:
                    material.order = int(new_order)  # Convert to integer
                    material.save()

            success_message = "Order updated successfully!"
            return render(request, 'reorder_course_material.html', {
                'course': course,
                'sessions': sessions,
                'materials': materials,
                'selected_session_id': selected_session_id,
                'success_message': success_message,
            })

    # Pass the course, sessions, and materials to the template
    return render(request, 'reorder_course_material.html', {
        'course': course,
        'sessions': sessions,
        'materials': materials,
        'selected_session_id': selected_session_id,
    })
def reading_material_detail(request, id):
    # Fetch the reading material by ID or return a 404 if it doesn't exist
    reading_material = get_object_or_404(ReadingMaterial, id=id)
    return render(request, 'reading_material_detail.html', {'reading_material': reading_material})

@login_required
def course_content(request, pk, session_id):
    course = get_object_or_404(Course, pk=pk)
    sessions = Session.objects.filter(course=course)

    # Fetch materials for the selected session
    selected_session_id = request.POST.get('session_id') or session_id
    session = get_object_or_404(Session, id=selected_session_id)
    materials = CourseMaterial.objects.filter(session=session).order_by('order')

    preview_url = None
    download_url = None
    file_type = None
    content_type = None
    file_id = None
    current_item = None
    next_item = None
    completion_status = False
    preview_content = None

    if 'file_id' in request.GET and 'file_type' in request.GET:
        file_id = request.GET.get('file_id')
        file_type = request.GET.get('file_type')

        if file_type == 'document':
            current_item = get_object_or_404(Document, id=file_id)
            file_url = current_item.doc_file.url
            content_type = 'document'
        elif file_type == 'video':
            current_item = get_object_or_404(Video, id=file_id)
            file_url = current_item.vid_file.url
            content_type = 'video'
        elif file_type == 'reading':
            current_item = get_object_or_404(ReadingMaterial, id=file_id)
            preview_url = True
            content_type = 'reading'
            preview_content = current_item.content

        # Find the next item
        current_material = materials.filter(material_id=file_id, material_type=file_type).first()
        if current_material:
            next_material = materials.filter(order__gt=current_material.order).first()
            if next_material:
                next_item = {
                    'type': next_material.material_type,
                    'id': next_material.material_id
                }

        # Check completion status
        completion = Completion.objects.filter(session=session, material__material_id=current_item.id, material__material_type=file_type).first()
        completion_status = completion.completed if completion else False

        if file_type in ['document', 'video']:
            file_name = os.path.basename(file_url)
            file_extension = os.path.splitext(file_name)[1].lower()
            previewable_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.ogg', '.pdf']
            if file_extension in previewable_extensions:
                preview_url = file_url
                if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                    content_type = 'image'
                elif file_extension in ['.mp4', '.webm', '.ogg']:
                    content_type = 'video'
                elif file_extension == '.pdf':
                    content_type = 'pdf'
            else:
                download_url = reverse('course:file_download', kwargs={'file_type': file_type, 'file_id': file_id})

    # Calculate completion percentage based on all materials
    all_materials = CourseMaterial.objects.filter(session__course=course)  # Fetch all materials across all sessions
    total_materials = all_materials.count()
    completed_materials = Completion.objects.filter(
        session__course=course,
        completed=True
    ).count()

    completion_percent = (completed_materials / total_materials) * 100 if total_materials > 0 else 0

    # Check if the course is completed and generate certificate
    certificate_url = None
    if completion_percent == 100:
        certificate_url = reverse('course:generate_certificate', kwargs={'pk': course.pk})

    context = {
        'course': course,
        'sessions': sessions,
        'materials': materials,  # Only show materials from the selected session
        'preview_url': preview_url,
        'download_url': download_url,
        'file_type': file_type,
        'content_type': content_type,
        'file_id': file_id,
        'current_item': current_item,
        'next_item': next_item,
        'completion_status': completion_status,
        'preview_content': preview_content,
        'certificate_url': certificate_url,
        'selected_session_id': selected_session_id,
    }

    return render(request, 'course_content.html', context)

@require_POST
@login_required
def toggle_completion(request, pk):
    course = get_object_or_404(Course, pk=pk)
    file_type = request.POST.get('file_type')
    file_id = request.POST.get('file_id')

    if file_type == 'document':
        content_object = get_object_or_404(Document, id=file_id, course=course)
    elif file_type == 'video':
        content_object = get_object_or_404(Video, id=file_id, course=course)
    elif file_type == 'reading':
        content_object = get_object_or_404(ReadingMaterial, id=file_id, course=course)
    else:
        return JsonResponse({'error': 'Invalid file type'}, status=400)

    completion, created = Completion.objects.get_or_create(
        course=course,
        **{file_type: content_object}
    )
    completion.completed = not completion.completed
    completion.save()

    documents = list(Document.objects.filter(course=course).order_by('id'))
    videos = list(Video.objects.filter(course=course).order_by('id'))
    reading_materials = list(ReadingMaterial.objects.filter(course=course).order_by('id'))

    next_item_type = None
    next_item_id = None

    if file_type == 'document':
        current_index = documents.index(content_object)
        if current_index < len(documents) - 1:
            next_item = documents[current_index + 1]
            next_item_type = 'document'
            next_item_id = next_item.id
        elif videos:
            next_item = videos[0]
            next_item_type = 'video'
            next_item_id = next_item.id
        elif reading_materials:
            next_item = reading_materials[0]
            next_item_type = 'reading'
            next_item_id = next_item.id
    elif file_type == 'video':
        current_index = videos.index(content_object)
        if current_index < len(videos) - 1:
            next_item = videos[current_index + 1]
            next_item_type = 'video'
            next_item_id = next_item.id
        elif reading_materials:
            next_item = reading_materials[0]
            next_item_type = 'reading'
            next_item_id = next_item.id
    elif file_type == 'reading':
        current_index = reading_materials.index(content_object)
        if current_index < len(reading_materials) - 1:
            next_item = reading_materials[current_index + 1]
            next_item_type = 'reading'
            next_item_id = next_item.id

    return JsonResponse({
        'completed': completion.completed,
        'next_item_type': next_item_type,
        'next_item_id': next_item_id
    })
# In course/views.py


def course_content_edit(request, pk, session_id):
    order = 1
    course = get_object_or_404(Course, pk=pk)
    sessions = Session.objects.filter(course=course)

    # Default to the first session if not specified in POST
    selected_session_id = request.POST.get('session_id') or session_id
    session = get_object_or_404(Session, id=selected_session_id)

    # Fetch materials associated with the selected session
    materials = CourseMaterial.objects.filter(session=session)
    #print("Materials associated with selected session:", [vars(material) for material in materials])  # List comprehension for material attributes

    # Get documents, videos, and reading materials based on the filtered materials
    document_ids = materials.filter(material_type='document').values_list('material_id', flat=True)
    video_ids = materials.filter(material_type='video').values_list('material_id', flat=True)
    reading_ids = materials.filter(material_type='reading').values_list('material_id', flat=True)

    documents = Document.objects.filter(id__in=document_ids)
    videos = Video.objects.filter(id__in=video_ids)
    reading_materials = ReadingMaterial.objects.filter(id__in=reading_ids)

    if request.method == 'POST':
        print("Session ID POST:", request.POST.get('session_id'))  # Debugging line
        # Process documents for deletion
        for document in documents:
            if f'delete_document_{document.id}' in request.POST:
                document.delete()

        # Process videos for deletion
        for video in videos:
            if f'delete_video_{video.id}' in request.POST:
                video.delete()

        # Process reading materials for deletion
        for reading_material in reading_materials:
            if f'delete_reading_material_{reading_material.id}' in request.POST:
                reading_material.delete()

        # Handle multiple document uploads
        doc_files = request.FILES.getlist('doc_file[]')
        doc_titles = request.POST.getlist('doc_title[]')
        for file, title in zip(doc_files, doc_titles):
            if file and title:
                document = Document.objects.create(
                    #material=None,  # Set the material reference later
                    doc_file=file,
                    doc_title=title
                )
                # Create a courseMaterial instance for the document
                course_material = CourseMaterial.objects.create(
                    session=session,
                    material_id=document.id,
                    material_type='document',
                    title=document.doc_title,
                    order=order
                )
                document.material = course_material  # Set the reverse relationship
                document.save()
                order += 1

        # Handle multiple video uploads
        vid_files = request.FILES.getlist('vid_file[]')
        vid_titles = request.POST.getlist('vid_title[]')
        for file, title in zip(vid_files, vid_titles):
            if file and title:
                video = Video.objects.create(
                    #material=None,  # Set the material reference later
                    vid_file=file,
                    vid_title=title
                )
                # Create a courseMaterial instance for the video
                course_material = CourseMaterial.objects.create(
                    session=session,
                    material_id=video.id,
                    material_type='video',
                    title=video.vid_title,
                    order=order
                )
                video.material = course_material  # Set the reverse relationship
                video.save()
                order += 1

        # Handle reading materials
        reading_material_titles = request.POST.getlist('reading_material_title[]')
        reading_material_contents = request.POST.getlist('reading_material_content[]')
        for title, content in zip(reading_material_titles, reading_material_contents):
            if title and content:
                reading_material = ReadingMaterial.objects.create(
                    material=None,  # Set the material reference later
                    title=title,
                    content=content
                )
                # Create a courseMaterial instance for the reading material
                course_material = CourseMaterial.objects.create(
                    session=session,
                    material_id=reading_material.id,
                    material_type='reading',
                    title=reading_material.title,
                    order=order
                )
                reading_material.material = course_material  # Set the reverse relationship
                reading_material.save()
                order += 1

        messages.success(request, 'course content updated successfully.')
        return redirect(reverse('course:course_content_edit', args=[course.pk, session.id]))

    # Context to render the template
    context = {
        'course': course,
        'sessions': sessions,
        'selected_session': session,
        'documents': documents,
        'videos': videos,
        'reading_materials': reading_materials,
    }

    return render(request, 'course_content_edit.html', context)

@login_required
def toggle_publish(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user == course.instructor or request.user.is_superuser:
        course.published = not course.published
        course.save()
    return redirect('course:course_detail', pk=pk)

@login_required
def generate_certificate_png(request, pk):
    course = get_object_or_404(Course, pk=pk)
    student = request.user

    # Verify that the student has completed the course
    total_materials = CourseMaterial.objects.filter(course=course).count()
    completed_materials = Completion.objects.filter(
        course=course,
        completed=True
    ).filter(
        Q(document__course=course) |
        Q(video__course=course) |
        Q(reading__course=course)
    ).distinct().count()

    if completed_materials != total_materials:
        return HttpResponse("You have not completed this course yet.", status=403)

    # Dynamically find the background image in the course app's static directory
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root of the project
    background_image_path = os.path.join(app_dir, 'course', 'static', 'course', 'images', 'certificate_background.jpg')

    if os.path.exists(background_image_path):
        with open(background_image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
    else:
        return HttpResponse(f"Background image not found at {background_image_path}", status=500)

    # Generate the certificate
    context = {
        'student_name': student.get_full_name() or student.username,
        'course_name': course.name,
        'completion_date': datetime.now().strftime("%B %d, %Y"),
        'background_image_base64': encoded_string,
    }

    return render(request, 'certificate_template.html', context)

