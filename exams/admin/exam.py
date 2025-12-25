from django.contrib import admin

from exams.models.exam import Exam, Question


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'duration', 'is_active', 'created')
    list_filter = ('is_active', 'created')
    search_fields = ('title', 'description')
    ordering = ('-created',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'text', 'correct_option', 'created')
    list_filter = ('exam', 'created')
    search_fields = ('text',)
    ordering = ('-created',)
