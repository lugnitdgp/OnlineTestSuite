from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=1024)    
    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question.title

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=14)
    rollno = models.CharField(max_length=10)

    def __str__(self):
        return self.rollno



