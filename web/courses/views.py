from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from courses.models import Course, Chapter, TextBlock, CodingProblem, UserSolution
from django.contrib.auth.models import User
# Create your views here.

@login_required
def courses(request):
    if User.get_user_permissions(request.user) == "admin":
        query = Course.objects.all()
    else:
        query = Course.objects.filter(public=True)

    context = {
        "courses": query,
    }

    return render(request, "courses/courses.html", context)

@login_required
def course(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    chapters = Chapter.objects.filter(course=course)
    #for each chapter get a coding problem
    for chapter in chapters:
        coding_problems = []
        chapter.coding_problems = CodingProblem.objects.filter(chapter=chapter)

    context = {
        "course": course,
        "chapters": chapters,
    }

    return render(request, "courses/course_detail.html", context)

@login_required
def chapter(request, course_slug, chapter_slug):
    chapter = Chapter.objects.get(slug=chapter_slug)
    text_blocks = TextBlock.objects.filter(chapter=chapter)
    context = {
        "chapter": chapter,
        "text_blocks": text_blocks,
    }

    return render(request, "courses/chapter.html", context)

@login_required
def coding_problem(request, course_slug, chapter_slug, coding_problem_slug):
    coding_problem = CodingProblem.objects.get(slug=coding_problem_slug)
    user_solutions = UserSolution.objects.filter(coding_problem=coding_problem).filter(user=request.user).order_by("submission_time")
    context = {
        "coding_problem": coding_problem,
        "user_solutions": user_solutions,
    }

    return render(request, "courses/coding_problem.html", context)