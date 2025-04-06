from django.contrib import admin

from users.models import Payment, User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "city")
    search_field = ("email",)
    ordering = ("email",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("date_of_payment", "payment_sum", "payment_method")
    search_field = ("date_of_payment",)
    ordering = ("date_of_payment",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "course")
    search_field = ("course",)
    ordering = ("course",)
