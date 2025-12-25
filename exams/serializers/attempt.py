from rest_framework import serializers
from django.core.exceptions import ValidationError
from exams.models import Answer


class AnswerCreateSerializer(serializers.ModelSerializer):
    selected_option = serializers.ChoiceField(choices=['A', 'B', 'C', 'D'])

    class Meta:
        model = Answer
        fields = (
            "question",
            "selected_option"
        )

    def validate(self, attrs):
        question = attrs.get("question")

        # Check question belongs to the exam of the attempt
        if question.exam.questions.filter(id=question.id).exists() is False:
            raise ValidationError("Question does not belong to the specified exam.")

        # Check question already answered in this attempt
        attempt = self.context.get('attempt')
        if Answer.objects.filter(attempt=attempt, question=question).exists():
            raise ValidationError("This question has already been answered in this attempt.")

        return super().validate(attrs)


class ExamResultSerializer(serializers.Serializer):

    score = serializers.IntegerField()
    submitted_at = serializers.DateTimeField(format="%d/%m/%Y %I:%M %p")
