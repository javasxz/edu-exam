from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimeStambedModel


class Exam(TimeStambedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")

    def __str__(self):
        return self.title


class Question(TimeStambedModel):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        indexes = [models.Index(fields=['exam'])]

    def __str__(self):
        return f"Question for {self.exam.title}"
