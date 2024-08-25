

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated,  AllowAny

from .utils import create_user_semesters
from .serializers import UserSerializer, UserPlanSerializer, UserSemesterSerializer, CreateUserSemesterSerializer
from .models import UserPlan, UserSemester


MAX_PLAN_NUMBER = 3


# User


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                "message": "User created successfully",
            }, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response({
                "message": "User creation failed",
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)


# User Plan


class UserPlanListCreateAPIView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication, JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return UserPlan.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        create_semesters = request.data.get('create', False)
        serializer = self.get_serializer(data=request.data)
        self.perform_create(serializer)
        plan_pk = serializer.data.get('pk', -1) or -1
        plan_type = serializer.data.get('type', '')
        user = request.user
        if create_semesters:
            create_user_semesters(plan_type, plan_pk, user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer: UserPlanSerializer):
        queryset = self.get_queryset()
        if len(list(queryset)) >= MAX_PLAN_NUMBER:
            raise ValidationError(f"You cannot create more than {
                                  MAX_PLAN_NUMBER} plans.")
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user)


class RetriveUserPlanView(generics.RetrieveAPIView):
    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication, JWTAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserPlan.objects.filter(owner=user)


class DeleteUserPlanAPIView(generics.RetrieveAPIView, generics.DestroyAPIView):
    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication, JWTAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserPlan.objects.filter(owner=user)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UpdateUserPlanAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication, JWTAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserPlan.objects.filter(owner=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer: UserPlanSerializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Plan updated successfully"})
        else:
            return Response({"message": "failed", "details": serializer.errors})


# User Semester

class UserSemesterListCreateAPIView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = CreateUserSemesterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication, JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return UserSemester.objects.filter(owner=user)

    def perform_create(self, serializer: CreateUserSemesterSerializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)


class RetriveUserSemesterAPIView(generics.RetrieveAPIView):
    serializer_class = UserSemesterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication, JWTAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserSemester.objects.filter(owner=user)


class UpdateUserSemesterAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = UserSemesterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication, JWTAuthentication]
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
        return Response({"message": "failed", "details": serializer.errors})


class DeleteUserSemesterAPIView(generics.RetrieveAPIView, generics.DestroyAPIView):
    serializer_class = UserSemesterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication, JWTAuthentication]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return UserSemester.objects.filter(owner=user)
