"""web URL Configuration

"""
from django.urls import re_path, include
from users.views import dashboard


urlpatterns = [
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    re_path(r"^dashboard/", dashboard, name="dashboard"),
]
