from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from exams.models import Exam, Question, ExamAttempt, Answer

User = get_user_model()


class ExamViewSetSuccessTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="student@gmail.com",
            password="112233"
        )
        self.client.force_authenticate(user=self.user)

        self.exam = Exam.objects.create(
            title="Sample Exam",
            description="A sample exam for testing",
            date=timezone.now().date(),
            duration=30,
            is_active=True
        )

        self.question1 = Question.objects.create(
            exam=self.exam,
            text="What is 1 + 1?",
            option_a="2",
            option_b="3",
            option_c="4",
            option_d="5",
            correct_option="A"
        )

        self.question2 = Question.objects.create(
            exam=self.exam,
            text="What is 2 + 2?",
            option_a="3",
            option_b="4",
            option_c="5",
            option_d="6",
            correct_option="B"
        )

    def test_exam_list_success(self):
        url = reverse("exams-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_exam_start_success(self):
        url = reverse("exams-start", args=[self.exam.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attempt_id", response.data)
        self.assertIn("questions", response.data)
        self.assertIn("saved_answers", response.data)

    def test_save_answer_success(self):
        attempt = ExamAttempt.objects.create(
            user=self.user,
            exam=self.exam,
            is_submitted=False,
            created=timezone.now()
        )

        url = reverse("exams-save-answer", args=[self.exam.id])
        payload = {
            "question": self.question1.id,
            "selected_option": "A"
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Answers saved successfully")
        self.assertEqual(Answer.objects.count(), 1)

    def test_exam_submit_success(self):
        attempt = ExamAttempt.objects.create(
            user=self.user,
            exam=self.exam,
            is_submitted=False,
            created=timezone.now()
        )

        Answer.objects.create(
            attempt=attempt,
            question=self.question1,
            selected_option="A"
        )

        Answer.objects.create(
            attempt=attempt,
            question=self.question2,
            selected_option="B"
        )

        url = reverse("exams-submit", args=[self.exam.id])
        response = self.client.post(url)

        attempt.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(attempt.is_submitted)
        self.assertEqual(attempt.score, 2)

    def test_exam_result_success(self):
        attempt = ExamAttempt.objects.create(
            user=self.user,
            exam=self.exam,
            is_submitted=True,
            score=2,
            submitted_at=timezone.now()
        )

        url = reverse("exams-result", args=[self.exam.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["score"], 2)
        self.assertIn("submitted_at", response.data)
