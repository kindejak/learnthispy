from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from courses.models import Course, Chapter, TextPart, CodingProblemPart, UserSolution, QuizPart, Part
from django.contrib.auth.models import User

import io
from contextlib import redirect_stdout

from pylint import epylint
import tempfile
import os
import json


from courses.utils import compare_texts

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
    chapters = course.chapters.all()
    print(chapters)
    context = {
        "course": course,
        "chapters": chapters,
    }
    print(context)

    return render(request, "courses/course_detail.html", context)

@login_required
def chapter(request, course_slug, chapter_slug):
    chapter = Chapter.objects.get(slug=chapter_slug)
    parts = chapter.parts.all().order_by("position")
    context = {
        "chapter": chapter,
        "parts": parts,
    }

    return render(request, "courses/chapter.html", context)


@login_required
def part(request, course_slug, chapter_slug, part_slug):
    part = Part.objects.get(slug=part_slug)
    chapter = Chapter.objects.get(slug=chapter_slug)
    parts = chapter.parts.all().order_by("position")

    if part.type == "text":
        part = TextPart.objects.get(slug=part_slug)
        context = {
        "part": part,
        "parts": parts,
        }
        return render(request, "courses/text.html", context)

    elif part.type == "coding_problem":
        coding_problem = CodingProblemPart.objects.get(slug=part_slug)
        user_solutions = UserSolution.objects.filter(coding_problem=coding_problem).filter(user=request.user).order_by("submission_time")
        user_last_solution = user_solutions.last()


        # compare user solution with expected output
        if user_last_solution:
            diff = compare_texts(user_last_solution.output, coding_problem.expected_output)
        else:
            diff = ""

        print(user_last_solution)

        context = {
            "parts": parts,
            "coding_problem": coding_problem,
            "user_solutions": list(user_solutions),
            "user_last_solution": user_last_solution,
            "diff": diff,
        }
        print(context)
        return render(request, "courses/coding_problem.html", context)
        

    elif part.type == "quiz":
        part = QuizPart.objects.get(slug=part_slug)
        parts = chapter.parts.all().order_by("position")
        context = {
            "part": part,
            "parts": parts,
        }
        return render(request, "courses/quiz.html", context)


@login_required
def submit_solution(request, course_slug, chapter_slug, coding_problem_slug):
    coding_problem_object = CodingProblemPart.objects.get(slug=coding_problem_slug)
    user_solution = UserSolution()
    user_solution.coding_problem = coding_problem_object
    user_solution.user = request.user
    user_solution.input = str(request.POST["code"])
    # run code
    with redirect_stdout(io.StringIO()) as f:
        try:
            exec(user_solution.input)
            user_solution.output = f.getvalue()
        except Exception as e:
            user_solution.error = e
            user_solution.output = e.__str__()
    user_solution.save()
    print(user_solution.output)
    # redirect to coding_problem
    return redirect("part",course_slug, chapter_slug, coding_problem_slug)

@csrf_exempt
def lint_code(request):
    # convert json to python dict
    data = json.loads(request.body)

    file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    file.write(data['code'])
    file.close()

    options = ' '.join([
        file.name,
        '--output-format', 'json',
        '--disable', 'C0114',
        '--disable', 'C0116', 
        '--disable', 'C0305',
        '--disable', 'C0103',
    ])

    (lint_stdout, lint_stderr) = epylint.py_run(return_std=True, command_options=options)

    os.remove(file.name)
    print(lint_stdout.getvalue())
    return HttpResponse(json.dumps(lint_stdout.getvalue()), content_type="application/json")