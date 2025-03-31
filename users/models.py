from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from materials.models import Course, Lesson


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("У пользователя должна быть почта")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите свою почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Укажите свой номер телефона",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите свой город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    CASH = "cash"
    BANK = "bank"

    STATUS_CHOICES = (
        (CASH, "Наличные"),
        (BANK, "Перевод на счет"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    date_of_payment = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата оплаты",
        help_text="Введите дату оплаты",
    )
    course_paid = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс оплачен",
        blank=True,
        null=True,
    )
    lesson_paid = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Урок оплачен",
        blank=True,
        null=True,
    )
    payment_sum = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        blank=True,
        null=True,
    )
    payment_method = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name="Способ оплаты"
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="id сессии",
        help_text="Укажите id сессии",
    )
    link = models.URLField(
        max_length=400,
        verbose_name="Ссылка на оплату",
        help_text="Добавьте ссылку на оплату",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.payment_sum


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Подписка на курс",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False, verbose_name="Статус подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
