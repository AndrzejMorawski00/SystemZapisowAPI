from rest_framework import serializers
from django.contrib.auth.models import User

from api.serializers import CourseReadOnlySerializer
from planner.utils import validate_passwords, validate_username

from .models import UserSemester, UserPlan


class UserSerializer(serializers.ModelSerializer):
    repeatPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'repeatPassword']
        extra_kwargs = {'password': {'write_only': True}, }

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        repeat_password = attrs.get('repeatPassword', '')
        error_messages = validate_username(username)
        error_messages.extend(validate_passwords(password, repeat_password))
        if error_messages:
            raise serializers.ValidationError({'errors': error_messages})
        return attrs

    def create(self, validated_data):
        validated_data.pop('repeatPassword')
        user = User.objects.create_user(**validated_data)
        return user


class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlan
        fields = ['pk', 'name', 'owner', 'type', 'slug']
        extra_kwargs = {'owner': {'read_only': True}}

    def to_representation(self, instance):
        result = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            semesters = map(lambda x: x.pk, list(
                UserSemester.objects.filter(owner=instance.owner, plan=instance)))
            result['semesters'] = semesters
        return result


class CreateUserSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSemester
        fields = '__all__'
        extra_kwargs = {'owner': {'read_only': True}, }


class UserSemesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSemester
        fields = '__all__'
        extra_kwargs = {'owner': {'read_only': True},
                        'plan': {'read_only': True}}

    def to_representation(self, instance):
        result = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            result['courses'] = CourseReadOnlySerializer(
                instance.courses.all(), many=True).data

        return result
