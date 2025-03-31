import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import Subscription, User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.pro")
        self.course = Course.objects.create(name="Курс 1", description="Полезный курс")
        self.lesson = Lesson.objects.create(
            name="Урок 1",
            courses=self.course,
            owner=self.user,
            link="https://www.youtube.com/watch?v=i3PdeDd9-KA",
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {
            "name": "Урок 2",
            "courses": self.course.pk,
            "link": "https://www.youtube.com/1",
        }
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"name": "Базовые функции Python"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Базовые функции Python")

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "link": self.lesson.link,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "courses": self.course.pk,
                    "owner": self.user.pk,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonUnauthorizedTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test_user1@mail.pro")
        self.course = Course.objects.create(
            name="Тестовый курс", description="Пробный курс"
        )
        self.lesson = Lesson.objects.create(
            name="Тестовый урок",
            courses=self.course,
            owner=self.user,
            link="https://youtu.be/dQw4w9WgXcQ",
        )

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_lesson_create(self):
    #     url = reverse("materials:lessons_create")
    #     data = {
    #         "name": "Тестовый урок 2",
    #         "courses": self.course.pk,
    #         "link": "https://www.youtube.com/2",
    #         "owner": self.user.pk
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"name": "Тестовый урок 1"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.pro")
        self.course = Course.objects.create(
            name="Курс 2", description="Интересный курс", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("users:course_subscription")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        message = {"message": "подписка добавлена"}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, message)
        self.assertEqual(Subscription.objects.all().count(), 1)

        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        message = {"message": "подписка удалена"}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, message)
        self.assertEqual(Subscription.objects.all().count(), 0)
