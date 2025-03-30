from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import URLValidator
from users.serializers import SubscriptionSerializer


class LessonSerializer(ModelSerializer):
    link = serializers.URLField(validators=[URLValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(source="lesson_set", many=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    counted_lessons = SerializerMethodField()
    lessons = LessonSerializer()
    subscription = SerializerMethodField()

    def get_count_lessons(self, course):
        return Course.objects.filter(lessons=course.lessons).count()

    def get_subscription(self, course):
        user = self.request.user
        subscription = Subscription.objects.filter(user=user, course=course)
        if subscription:
            return subscription.is_active
        else:
            return False

    class Meta:
        model = Course
        fields = ("name", "description", "counted_lessons", "lessons", "subscription")
