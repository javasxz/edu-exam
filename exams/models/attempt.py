from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimeStambedModel


class ExamAttempt(TimeStambedModel):
    user = models.ForeignKey(
        'users.User',
        related_name='exams',
        on_delete=models.CASCADE
    )
    exam = models.ForeignKey(
        'exams.Exam',
        related_name='attempts',
        on_delete=models.CASCADE
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Exam Attempt")
        verbose_name_plural = _("Exam Attempts")
        unique_together = ("user", "exam")

    def __str__(self):
        return f"Attempt by {self.user} for {self.exam}"


class Answer(models.Model):
    attempt = models.ForeignKey(
        ExamAttempt,
        related_name="answers",
        on_delete=models.CASCADE
    )
    question = models.ForeignKey('exams.Question', on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    is_late_submission = models.BooleanField(default=False)
    locked = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        unique_together = ("attempt", "question")

    def __str__(self):
        return f"Answer to {self.question} in {self.attempt}"
