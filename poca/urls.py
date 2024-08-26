from django.contrib import admin
from django.urls import path, include

from users.views import RegisterView, LoginView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", RegisterView.as_view(), name="user registration"),
    path("auth/token/", LoginView.as_view(), name="user login"),
    path("photo-cards/", include("photo_cards.urls")),
]
