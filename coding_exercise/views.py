from django.shortcuts import render, get_object_or_404, redirect
from coding_exercise.models import Exercise#, Submission
from coding_exercise.forms import ExerciseForm#, SubmissionForm

from exercises.models import Submission
from exercises.forms import SubmissionForm
from django.contrib.auth.decorators import login_required

# View to list all exercises
def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'exercise_list1.html', {'exercises': exercises})

def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    return render(request, 'exercise_detail.html', {'exercise': exercise})

@login_required
def exercise_edit(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('coding_exercise:exercise_detail', exercise_id=exercise.id)
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'exercise_form.html', {'form': form, 'exercise': exercise})

@login_required
def exercise_delete(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise.delete()
        return redirect('exercises:exercise_list')
    return render(request, 'exercise_confirm_delete.html', {'exercise': exercise})

# View to create a new exercise (admin)
@login_required
def exercise_add(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coding_exercise:exercise_list')  # Ensure the correct namespace for your URL here
    else:
        form = ExerciseForm()

    return render(request, 'exercise_form1.html', {'form': form})

# View for a student to submit code for an exercise
@login_required
def submit_exercise(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.exercise = exercise
            submission.save()
            return redirect('exercise_list')
    else:
        form = SubmissionForm()
    return render(request, 'submit_exercise.html', {'form': form, 'exercise': exercise})

# View to display all submissions
@login_required
def submission_list(request):
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'submission_list.html', {'submissions': submissions})
