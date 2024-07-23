from rest_framework import serializers
from django.contrib.auth.models import User

from .models import UserSemester, UserPlan


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class UserPlanSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = UserPlan
        fields = ['pk', 'name', 'owner', 'type']
        extra_kwargs = {'owner': {'read_only': True}}


class CreateUserSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSemester
        fields = '__all__'
        extra_kwargs = {'owner': {'read_only': True}, }

class UserSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSemester
        fields = '__all__'
        extra_kwargs = {'owner': {'read_only': True}, 'plan' : {'read_only' : True}}



# class UserSemesterSerializer(serializers.Serializer):
#     owner = UserSerializer()
#     plan = serializers.PrimaryKeyRelatedField()
#     courses = serializers.PrimaryKeyRelatedField(many=True)
#     class Meta:
#         model = UserSemester
#         fields = '__all__'
#         extra_kwargs = {'owner': {'read_only': True}}
