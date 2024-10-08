from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from rest_framework import generics

from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend


from .filters import CourseFilter
from .pagination import StandardResultSetPagination
from .serializers import CourseSerializer, SemesterSerializer, CourseTagSerializer, CourseEffectSerializer, CourseTypeSerializer, CourseReadOnlySerializer
from panel.models import Semester, CourseType, CourseTag, CourseEffect, Course

from api.constants import api_endpoints

# Create your views here.


def index(request: HttpRequest):
    return render(request, 'api/home.html', {'api_endpoints': api_endpoints})


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
    pagination_class = StandardResultSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_class = CourseFilter
    permission_classes = [AllowAny]

    def get_queryset(self):
        semester_id = self.kwargs.get('semester_pk')
        if semester_id:
            try:
                semester = Semester.objects.get(pk=semester_id)
                return Course.objects.filter(semester=semester).order_by('name')
            except Semester.DoesNotExist:
                return Course.objects.none()
        return Course.objects.none()


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        course_id = self.kwargs.get('course_pk')
        if course_id:
            try:
                return Course.objects.get(pk=course_id)
            except Course.DoesNotExist:
                raise Course.DoesNotExist("Course doesn't exists")
        raise Exception("Didn't provide course pk")
