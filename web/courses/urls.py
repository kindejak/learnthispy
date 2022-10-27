"""web URL Configuration

"""
from django.urls import re_path, include, path
from courses.views import courses, course, chapter, coding_problem, submit_solution


urlpatterns = [
    re_path(r"^courses/$", courses, name="courses"),
    path("courses/<slug:course_slug>/", course, name="course"),
    path("courses/<slug:course_slug>/<slug:chapter_slug>/", chapter, name="chapter"),
    path("courses/<slug:course_slug>/<slug:chapter_slug>/<slug:coding_problem_slug>/", coding_problem, name="coding_problem"),
    path("courses/<slug:course_slug>/<slug:chapter_slug>/<slug:coding_problem_slug>/submit", submit_solution, name="submit_solution"),
]