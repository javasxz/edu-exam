from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from exams.models import Exam
from exams.serializers import ExamListSerializer, ExamDetailSerializer


class ExamViewSet(viewsets.ViewSet):
    queryset = Exam.objects.all()
    serializer_classes = {
        "list": ExamListSerializer,
        "retrieve": ExamDetailSerializer,
    }

    def get_queryset(self):
        return Exam.objects.filter(is_active=True)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ExamListSerializer)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        exam = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer_class()(exam)
        return Response(serializer.data)

    