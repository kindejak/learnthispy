from enum import unique
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=40,null=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    students = models.ManyToManyField(User, related_name="students", blank=True)
        
    def __str__(self):
        return self.title

# chapters
class Chapter(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=40,null=True,unique=True)

    def __str__(self):
        return self.title


# text_blocks
class TextBlock(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=40,null=True)

class CodingProblem(models.Model):
    title = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,null = True)
    description = models.TextField()
    time_limit = models.IntegerField(default=10)
    memory_limit = models.IntegerField(default=256)
    output = models.TextField(blank=True, null=False)
    deadline = models.DateTimeField(blank=True, null=True)
    code_template = models.TextField(blank=True, null=False)    
    slug = models.SlugField(max_length=40,null=True,unique=True)

    def __str__(self):
        return self.title
    
    
class UserSolution(models.Model):
    coding_problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE)
    input = models.TextField(blank=True, null=False)
    output = models.TextField(blank=True, null=False)
    coding_problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now_add=True)
    error = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.user.username + " " + self.coding_problem.title + " " + str(self.submission_time)