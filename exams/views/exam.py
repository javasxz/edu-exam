from rest_framework import viewsets
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from exams.models import Exam, Question, ExamAttempt, Answer
from django.utils import timezone
from datetime import timedelta
from exams.serializers import (
    ExamListSerializer,
    QuestionListSerializer,
    AnswerCreateSerializer,
    ExamResultSerializer
)


class ExamViewSet(viewsets.ViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamListSerializer

    def get_queryset(self):
        return Exam.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def start(self, request, pk=None):

        exam = get_object_or_404(self.get_queryset(), pk=pk)

        attempt, _ = ExamAttempt.objects.get_or_create(
            user=request.user,
            exam=exam,
            is_submitted=False
        )

        # Validate exam time constraint
        if exam.is_exam_ended(attempt.created):
            return Response({"detail": "Exam time expired"}, status=403)

        saved_answers = {ans.question_id: ans.selected_option for ans in attempt.answers.all()}

        questions = Question.objects.filter(exam=exam)
        serializer = QuestionListSerializer(questions, many=True)

        return Response({
            "attempt_id": attempt.id,
            "questions": serializer.data,
            "saved_answers": saved_answers
        })

    @action(methods=["post"], detail=True, url_path="save-answer")
    @transaction.atomic
    def save_answer(self, request, pk=None):
        exam = get_object_or_404(self.get_queryset(), pk=pk)
        attempt = get_object_or_404(
            ExamAttempt,
            user=request.user,
            exam=exam,
            is_submitted=False
        )

        serializer = AnswerCreateSerializer(data=request.data, context={"attempt": attempt})
        serializer.is_valid(raise_exception=True)

        # Check answer is submitted within allowed time or not
        is_late_submission = False
        if timezone.now() > attempt.created + timedelta(minutes=exam.duration):
            is_late_submission = True
    
        Answer.objects.create(
            attempt=attempt,
            question=serializer.validated_data["question"],
            selected_option=serializer.validated_data["selected_option"],
            is_late_submission=is_late_submission
        )

        return Response({"status": "Answers saved successfully"})

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def submit(self, request, pk=None):
        exam = get_object_or_404(self.get_queryset(), pk=pk)

        attempt = get_object_or_404(
            ExamAttempt,
            user=request.user,
            exam=exam,
            is_submitted=False
        )

        # Time enforcement
        if timezone.now() > attempt.created + timedelta(minutes=exam.duration):
            return Response({"detail": "Exam time expired"}, status=403)

        answers = attempt.answers.select_related("question")

        score = sum(1 for ans in answers if ans.selected_option == ans.question.correct_option)

        attempt.score = score
        attempt.is_submitted = True
        attempt.submitted_at = timezone.now()
        attempt.save(update_fields=["score", "is_submitted", "submitted_at"])

        return Response({"detail": "Exam submitted successfully"})

    @action(methods=["get"], detail=True)
    def result(self, request, pk=None):
        exam = get_object_or_404(self.get_queryset(), pk=pk)
        attempt = ExamAttempt.objects.filter(
            user=request.user,
            exam=exam,
            is_submitted=True
        )
        if not attempt.exists():
            return Response({"detail": "No exam result found"}, status=404)

        serializer = ExamResultSerializer({
            "score": attempt.score,
            "submitted_at": attempt.submitted_at
        })

        return Response(serializer.data)
