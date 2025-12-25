from rest_framework import serializers

from exams.models import Exam, Question


class ExamListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = [
            "id",
            "title",
            "description",
            "date",
            "duration"
        ]


class QuestionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
        ]


class ExamDetailSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = [
            "id",
            "title",
            "description",
            "date",
            "duration",
            "questions",
        ]


