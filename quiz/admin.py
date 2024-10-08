from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Quiz, Question, AnswerOption, StudentQuizAttempt, StudentAnswer, AIGrading
from course.models import Course  # Import the Course model



class QuizResource(resources.ModelResource):
    class Meta:
        model = Quiz
        fields = ('id', 'course__course_name', 'quiz_title', 'quiz_description', 'total_marks', 
                  'time_limit', 'created_by__username', 'created_at', 'updated_at', 
                  'start_datetime', 'end_datetime', 'attempts_allowed')


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        fields = ('id', 'quiz__quiz_title', 'question_text', 'question_type', 'points')


class AnswerOptionResource(resources.ModelResource):
    class Meta:
        model = AnswerOption
        fields = ('id', 'question__question_text', 'option_text', 'is_correct')


class StudentQuizAttemptResource(resources.ModelResource):
    class Meta:
        model = StudentQuizAttempt
        fields = ('id', 'user__username', 'quiz__quiz_title', 'score', 'attempt_date', 
                  'is_proctored', 'proctoring_data')


class StudentAnswerResource(resources.ModelResource):
    class Meta:
        model = StudentAnswer
        fields = ('id', 'attempt__quiz__quiz_title', 'question__question_text', 
                  'selected_option__option_text', 'text_response')


class AIGradingResource(resources.ModelResource):
    class Meta:
        model = AIGrading
        fields = ('id', 'answer__question__question_text', 'feedback_text', 'awarded_points')


@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin):
    resource_class = QuizResource
    list_display = ('quiz_title', 'course', 'total_marks', 'created_by', 'created_at')
    search_fields = ('quiz_title', 'course__course_name', 'created_by__username')
    list_filter = ('course', 'created_by', 'created_at')


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ('question_text', 'quiz', 'question_type', 'points')
    search_fields = ('question_text', 'quiz__quiz_title')
    list_filter = ('quiz', 'question_type')


@admin.register(AnswerOption)
class AnswerOptionAdmin(ImportExportModelAdmin):
    resource_class = AnswerOptionResource
    list_display = ('option_text', 'question', 'is_correct')
    search_fields = ('option_text', 'question__question_text')
    list_filter = ('question__quiz', 'is_correct')


@admin.register(StudentQuizAttempt)
class StudentQuizAttemptAdmin(ImportExportModelAdmin):
    resource_class = StudentQuizAttemptResource
    list_display = ('user', 'quiz', 'score', 'attempt_date', 'is_proctored')
    search_fields = ('user__username', 'quiz__quiz_title')
    list_filter = ('quiz', 'user', 'attempt_date')


@admin.register(StudentAnswer)
class StudentAnswerAdmin(ImportExportModelAdmin):
    resource_class = StudentAnswerResource
    list_display = ('attempt', 'question', 'selected_option', 'text_response')
    search_fields = ('attempt__user__username', 'question__question_text', 'selected_option__option_text')
    list_filter = ('attempt__quiz', 'question')


@admin.register(AIGrading)
class AIGradingAdmin(ImportExportModelAdmin):
    resource_class = AIGradingResource
    list_display = ('answer', 'feedback_text', 'awarded_points')
    search_fields = ('answer__question__question_text', 'feedback_text')
    list_filter = ('awarded_points',)
