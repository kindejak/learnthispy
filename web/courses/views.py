from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from courses.models import Course, Chapter, TextBlock
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
    query = Chapter.objects.filter(course=course)
    context = {
        "course": course,
        "chapters": query,
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