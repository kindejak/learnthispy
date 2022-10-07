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
    content = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
