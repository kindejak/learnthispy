"""web URL Configuration

"""
from django.urls import re_path, include, path
from courses.views import courses, course, chapter, submit_solution, part,lint_code


urlpatterns = [
    path("lint/", lint_code, name="lint_code"),
    re_path(r"^courses/$", courses, name="courses"),
    path("courses/<slug:course_slug>/", course, name="course"),
    path("courses/<slug:course_slug>/<slug:chapter_slug>/", chapter, name="chapter"),
    path("courses/<slug:course_slug>/<slug:chapter_slug>/<slug:part_slug>/", part, name="part"),
    path("courses/<slug:course_slug>/<slug:chapter_slug>/<slug:coding_problem_slug>/submit/", submit_solution, name="submit_solution"),

]