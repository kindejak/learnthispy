from enum import unique
from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class Part(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=40,null=True,unique=True)
    type = models.CharField(max_length=100, default="")
    position = models.IntegerField(default=999)

    def __str__(self):
        return self.title

# chapters
class Chapter(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=40,null=True,unique=True)
    parts = models.ManyToManyField(Part, related_name="parts", blank=True)

    def __str__(self):
        return self.title


# text_blocks
class TextPart(Part):
    content = models.TextField()




class CodingProblemPart(Part):
    description = models.TextField()
    time_limit = models.IntegerField(default=10)
    memory_limit = models.IntegerField(default=256)
    output = models.TextField(blank=True, null=False)
    deadline = models.DateTimeField(blank=True, null=True)
    code_template = models.TextField(blank=True, null=False)    
 
    
    def __str__(self):
        return self.title

class UserSolution(models.Model):
    coding_problem = models.ForeignKey(CodingProblemPart, null=True,default=None, on_delete=models.CASCADE)
    input = models.TextField(blank=True, null=False)
    output = models.TextField(blank=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now_add=True)
    error = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.user.username + " " + self.coding_problem.title + " " + str(self.submission_time)

# is stored in Json format like this:
# {
#     "question": "What is the output of the following code?",
#     "options": [
#         "1",
#         "2",
#         "3"
#      ],
#     "answer": [
#           "2",
#           "3"
#      ]
class Question(models.Model):
    json_question = models.TextField()

class QuizPart(Part):
    deadline = models.DateTimeField(blank=True, null=True)
    questions = models.ManyToManyField(Question, related_name="questions", blank=True)
    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=40,null=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    chapters = models.ManyToManyField(Chapter,"Chapter", blank=True)
    students = models.ManyToManyField(User, related_name="students", blank=True)
        
    def __str__(self):
        return self.title