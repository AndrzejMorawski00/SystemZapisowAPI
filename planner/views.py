from django.shortcuts import render

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import UserPlanSerializer, UserSemesterSerializer, CreateUserSemesterSerializer
from .models import UserPlan, UserSemester
from panel.models import Course

MAX_PLAN_NUMBER = 3
MAX_SEMESTER_NUMBER = 10

# User Plan


class UserPlanListCreateAPIView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return UserPlan.objects.filter(owner=user)

    def perform_create(self, serializer: UserPlanSerializer):
        queryset = self.get_queryset()
        if len(list(queryset)) >= MAX_PLAN_NUMBER:
            raise ValidationError(f"You cannot create more than {
                                  MAX_PLAN_NUMBER} plans.")
        if serializer.is_valid():
            serializer.save(owner=self.request.user)


class RetriveUserPlanView(generics.RetrieveAPIView):
    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserPlan.objects.filter(owner=user)


class DeleteUserPlanAPIView(generics.RetrieveAPIView, generics.DestroyAPIView):
    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserPlan.objects.filter(owner=user)


class UpdateUserPlanAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserPlan.objects.filter(owner=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer: UserPlanSerializer = self.get_serializer(
            instance, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Plan updated successfully"})

        else:
            return Response({"message": "failed", "details": serializer.errors})


# User Semester

class UserSemesterListCreateAPIView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = CreateUserSemesterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return UserSemester.objects.filter(owner=user)

    def perform_create(self, serializer: CreateUserSemesterSerializer):
        queryset = self.get_queryset()
        if len(list(queryset)) >= MAX_SEMESTER_NUMBER:
            raise ValidationError(f"You cannot create more than {
                                  MAX_SEMESTER_NUMBER} semesters.")
        if serializer.is_valid():
            serializer.save(owner=self.request.user)


class RetriveUserSemesterAPIView(generics.RetrieveAPIView):
    serializer_class = UserSemesterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserSemester.objects.filter(owner=user)


class UpdateUserSemesterAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = UserSemesterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserSemester.objects.filter(owner=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer: UserSemesterSerializer = self.get_serializer(
            instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Plan updated successfully"})

        else:
            return Response({"message": "failed", "details": serializer.errors})


class DeleteUserSemesterAPIView(generics.RetrieveAPIView, generics.DestroyAPIView):
    serializer_class = UserSemesterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserSemester.objects.filter(owner=user)
