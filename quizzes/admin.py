from django.contrib import admin
from .models import *

# Inline for Questions within Quiz
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of empty question forms to display
    fields = ('text', 'option1', 'option2', 'option3', 'option4', 'correct_option')
    show_change_link = True

# Admin for Quiz
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'question_count')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    inlines = [QuestionInline]

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'

# Admin for Question
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'correct_option')
    list_filter = ('quiz',)
    search_fields = ('text',)
    list_per_page = 25

# Admin for UserAttempt
@admin.register(UserAttempt)
class UserAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'attempted_at')
    list_filter = ('quiz', 'user', 'attempted_at')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = ('score', 'attempted_at')
    list_per_page = 25

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct')
    list_filter = ('attempt', 'question')