from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, UserCourseProgress, User
from .forms import CourseForm, UserCourseProgressForm
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from user.models import User 

def course_list(request):
    query = request.GET.get('q', '')
    selected_creator = request.GET.get('created_by', '')

    courses = Course.objects.all()
    created_by_list = User.objects.values_list('username', flat=True).distinct()

    if query and selected_creator:
        courses = courses.filter(
            Q(course_name__icontains=query),
            created_by__username=selected_creator 
        )
    elif query:
        courses = courses.filter(Q(course_name__icontains=query))
    elif selected_creator:
        courses = courses.filter(created_by__username=selected_creator)  

    not_found = not courses.exists()

    return render(request, 'course_list.html', {
        'courses': courses,
        'query': query,
        'created_by_list': created_by_list,
        'selected_creator': selected_creator,
        'not_found': not_found,
    })

def course_detail(request, pk):
    """Display details about a course and user progress in that course."""
    course = get_object_or_404(Course, pk=pk)
    
    user_query = request.GET.get('user', '')
    selected_progress = request.GET.get('progress', '')

    user_progress = UserCourseProgress.objects.filter(course=course)

    if user_query and selected_progress:
        user_progress = user_progress.filter(
            Q(user__username__icontains=user_query) | Q(user__full_name__icontains=user_query),
            progress_percentage__in=get_progress_range(selected_progress)
        )
    elif user_query:
        user_progress = user_progress.filter(
            Q(user__username__icontains=user_query) | Q(user__full_name__icontains=user_query)
        )
    elif selected_progress:
        user_progress = user_progress.filter(progress_percentage__in=get_progress_range(selected_progress))

    not_found = not user_progress.exists()

    return render(request, 'course_detail.html', {
        'course': course,
        'user_progress': user_progress,
        'user_query': user_query,
        'selected_progress': selected_progress,
        'not_found': not_found,
    })

def get_progress_range(selected_progress):
    """Return the appropriate progress range based on the selected option."""
    if selected_progress == 'under_50':
        return range(0, 50)
    elif selected_progress == '50_to_90':
        return range(50, 90)
    elif selected_progress == 'over_90':
        return range(91, 101)
    elif selected_progress == '100':
        return [100]  
    return []



def course_add(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course_form.save()
            return redirect('course:course_list')  
    else:
        course_form = CourseForm()
    
    return render(request, 'course_form.html', {'course_form': course_form})

def course_edit(request, pk):
    """Chỉnh sửa thông tin của một khóa học cụ thể."""
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        course_form = CourseForm(request.POST, instance=course)
        if course_form.is_valid():
            course_form.save()
            return redirect('course:course_list')
    else:
        course_form = CourseForm(instance=course)
    
    return render(request, 'course_form.html', {'course_form': course_form})

def course_delete(request, pk):
    """Xóa một khóa học cụ thể."""
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        course.delete()
        return redirect('course:course_list') 
    
    return render(request, 'course_confirm_delete.html', {'course': course})

def delete_user_progress(request, course_id, user_id):
    user_progress = get_object_or_404(UserCourseProgress, course_id=course_id, user_id=user_id)
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        user_progress.delete()
        return redirect('course:course_detail', pk=course.pk)  

    return render(request, 'course_confirm_delete.html', {
        'user': user_progress.user,
        'course': course
    })

def create_progress(request, course_id):
    """Tạo tiến độ của người dùng trong một khóa học cụ thể."""
    course = get_object_or_404(Course, pk=course_id) 
    users = User.objects.all() 

    if request.method == 'POST':
        progress_form = UserCourseProgressForm(request.POST)
        if progress_form.is_valid():
            user = progress_form.cleaned_data['user']
            progress_percentage = progress_form.cleaned_data['progress_percentage']
            UserCourseProgress.objects.create(
                user=user,
                course=course,
                progress_percentage=progress_percentage
            )
            messages.success(request, 'Progress created successfully.')
            return redirect('course:course_detail', pk=course_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        progress_form = UserCourseProgressForm()

    return render(request, 'create_progress.html', {'form': progress_form, 'course': course, 'users': users})

def update_progress_percentage(request, course_id, user_id):
    """Cập nhật tiến độ của người dùng trong một khóa học cụ thể."""
    course = get_object_or_404(Course, pk=course_id)
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        progress_percentage = request.POST.get('progress_percentage')

        progress, created = UserCourseProgress.objects.update_or_create(
            user=user, course=course,
            defaults={'progress_percentage': progress_percentage, 'last_accessed': timezone.now()}
        )
        
        if created:
            print("Progress created successfully.")
        else:
            print("Progress updated successfully.")
        
        return redirect('course:course_detail', pk=course_id)
    
    progress = UserCourseProgress.objects.filter(user=user, course=course).first()
    
    return render(request, 'update_progress_percentage.html', {
        'course': course,
        'user': user,
        'progress': progress
    })