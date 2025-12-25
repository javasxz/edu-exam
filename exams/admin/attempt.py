from django.contrib import admin

from exams.models import ExamAttempt, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'exam', 'is_submitted', 'submitted_at', 'score', 'created')
    list_filter = ('is_submitted', 'created')
    search_fields = ('user__email', 'exam__title')
    inlines = [AnswerInline]
    ordering = ('-created',)
