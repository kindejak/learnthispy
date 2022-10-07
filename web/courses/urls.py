"""web URL Configuration

"""
from django.urls import re_path, include, path
from courses.views import courses, course, chapter


urlpatterns = [
    re_path(r"^courses/$", courses, name="courses"),
    path("courses/<slug:course_slug>/", course, name="course"),
    path("courses/<slug:course_slug>/<slug:chapter_slug>", chapter, name="chapter"),
]