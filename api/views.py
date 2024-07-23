from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


from .serializers import SemesterSerializer, CourseTagSerializer, CourseEffectSerializer, CourseTypeSerializer, CourseReadOnlySerializer
from panel.models import Semester, CourseType, CourseTag, CourseEffect, Course

# Create your views here.


def index(request: HttpRequest):
    return render(request, 'api/home.html', {})


def api_view(request: HttpRequest):
    return HttpResponse('API Sweet Api')


class CourseTagListAPIView(generics.ListAPIView, ):
    serializer_class = CourseTagSerializer
    permission_classes = [AllowAny]
    queryset = CourseTag.objects.all()


class CourseTagRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseTagSerializer
    permission_classes = [AllowAny]
    queryset = CourseTag.objects.all()
    lookup_field = 'pk'


class CourseTypeListAPIView(generics.ListAPIView):
    serializer_class = CourseTypeSerializer
    permission_classes = [AllowAny]
    queryset = CourseType.objects.all()


class CourseTypeRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseTypeSerializer
    permission_classes = [AllowAny]
    queryset = CourseType.objects.all()
    lookup_field = 'pk'


class CourseEffectListAPIView(generics.ListAPIView):
    serializer_class = CourseEffectSerializer
    permission_classes = [AllowAny]
    queryset = CourseEffect.objects.all()


class CourseEffectRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseEffectSerializer
    permission_classes = [AllowAny]
    queryset = CourseEffect.objects.all()
    lookup_field = 'pk'


class SemesterListAPIView(generics.ListAPIView):
    serializer_class = SemesterSerializer
    permission_classes = [AllowAny]
    queryset = Semester.objects.all()


class SemesterRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = SemesterSerializer
    permission_classes = [AllowAny]
    queryset = Semester.objects.all()
    lookup_field = 'pk'


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseReadOnlySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        semester_id = self.kwargs.get('semester_id')
        if semester_id:
            try:
                semester = Semester.objects.get(pk=semester_id)
                return Course.objects.filter(semester=semester).order_by('name')
            except Semester.DoesNotExist:
                return None
        return None
