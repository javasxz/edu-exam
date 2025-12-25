from django.contrib import admin

from exams.models.exam import Exam, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'duration', 'is_active', 'created')
    list_filter = ('is_active', 'created')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    ordering = ('-created',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'text', 'correct_option', 'created')
    list_filter = ('exam', 'created')
    search_fields = ('text',)
    ordering = ('-created',)
