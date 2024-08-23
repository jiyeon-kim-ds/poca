from django.contrib import admin
from django.urls import path

from users.views import RegisterView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", RegisterView.as_view(), name="user registration"),
]
