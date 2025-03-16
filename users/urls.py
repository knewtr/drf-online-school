from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig

from users.views import UserViewSet, PaymentCreateAPIView, PaymentRetrieveAPIView, PaymentListAPIView, PaymentUpdateAPIView, PaymentDestroyAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payments_create"),
    path("payments/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payments_retrieve"),
    path("payments/<int:pk>/update/", PaymentUpdateAPIView.as_view(), name="payments_update"),
    path("payments/<int:pk>/delete/", PaymentDestroyAPIView.as_view(), name="payments_delete"),
]
urlpatterns += router.urls
