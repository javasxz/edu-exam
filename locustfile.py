import random

from locust import HttpUser, task, between
from locust.exception import StopUser

DISCONNECT_PROBABILITY = 0.1


import random
from locust import HttpUser, task, between
from locust.exception import StopUser

DISCONNECT_PROBABILITY = 0.1


class ExamUser(HttpUser):
    wait_time = between(1, 3)

    exam_id = None
    attempt_id = None
    questions = []
    answered = set()
    is_exam_loaded = False

    def on_start(self):
        self._authenticate()
        self._select_exam()
        self._start_or_resume_exam()

    def _authenticate(self):
        self.username = f"user_{random.randint(1, 50)}@example.com"
        self.password = "testing321"

        res = self.client.post(
            "/api/v1/auth/token/",
            json={
                "username": self.username,
                "password": self.password,
            },
            name="Auth Token"
        )

        if res.status_code != 200:
            print(res.text)
            raise StopUser()

        token = res.json()["data"]["token"]
        self.client.headers.update({
            "Authorization": f"Token {token}"
        })

    def _select_exam(self):
        res = self.client.get("/api/v1/exams/", name="List Exams")

        if res.status_code != 200:
            raise StopUser()

        exams = res.json()["data"]
        if not exams:
            raise StopUser()

        self.exam_id = random.choice(exams)["id"]

    def _start_or_resume_exam(self):
        res = self.client.post(
            f"/api/v1/exams/{self.exam_id}/start/",
            name="Start / Resume Exam"
        )

        if res.status_code != 200:
            raise StopUser()

        data = res.json()["data"]
        self.attempt_id = data["attempt_id"]
        self.questions = data["questions"]

        saved = data.get("saved_answers", {})
        self.answered = {int(qid) for qid in saved.keys()}
        self.is_exam_loaded = True

    @task(5)
    def answer_question(self):

        if not self.is_exam_loaded:
            return

        unanswered = [
            q for q in self.questions
            if q["id"] not in self.answered
        ]

        if not unanswered:
            self.submit_exam()
            return

        question = random.choice(unanswered)
        option = random.choice(question["options"])

        res = self.client.post(
            f"/api/v1/exams/{self.exam_id}/save-answer/",
            json={
                "question": question["id"],
                "selected_option": option["id"],
            },
            name="Submit Answer"
        )

        if res.status_code == 200:
            self.answered.add(question["id"])

        if random.random() < DISCONNECT_PROBABILITY:
            raise StopUser()

    @task(1)
    def submit_exam(self):
        res = self.client.post(
            f"/api/v1/exams/{self.exam_id}/submit/",
            name="Submit Exam"
        )

        if res.status_code == 200:
            raise StopUser()

    @task(1)
    def get_result(self):
        res = self.client.get(
            f"/api/v1/exams/{self.exam_id}/result/",
            name="View Exam Results"
        )
        print('res.status_code', res.status_code)
        if res.status_code == 200:
            raise StopUser()
