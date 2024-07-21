from rest_framework import serializers

from panel.models import Semester, CourseType, CourseTag, CourseEffect, Course


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['pk', 'name']


class CourseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTag
        fields = '__all__'


class CourseEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEffect
        fields = '__all__'


class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    effects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['pk', 'name', 'recommended_for_first_year',
                  'type', 'ects', 'tags', 'effects']
