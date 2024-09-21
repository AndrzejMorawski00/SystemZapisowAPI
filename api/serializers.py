from rest_framework import serializers

from panel.models import Semester, CourseType, CourseTag, CourseEffect, Course


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name']


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
        fields = ['id', 'name','url', 'recommended_for_first_year',
                  'type', 'ects', 'tags', 'effects']


class CourseReadOnlySerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    effects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name','url', 'recommended_for_first_year',
                  'type', 'ects', 'tags', 'effects']

    def to_representation(self, instance):
        result = super().to_representation(instance)
        type_id = result.get('type', -1)
        tags = result.get('tags', [])
        effects = result.get('effects', [])
        try:
            fetched_type = CourseTypeSerializer(
                CourseType.objects.get(pk=type_id)).data
            fetched_tags = CourseTagSerializer(
                list(CourseTag.objects.filter(pk__in=tags)), many=True).data
            fetched_effects = CourseEffectSerializer(
                list(CourseEffect.objects.filter(id__in=effects)), many=True).data
        except (CourseType.DoesNotExist):
            return result
        result['type'] = fetched_type
        result['tags'] = fetched_tags
        result['effects'] = fetched_effects
        return result
