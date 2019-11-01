from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=1024)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        str_repr = self.text[:51] + \
            "..." if (len(self.text) >= 52) else self.text
        return str_repr


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time_elapsed = models.IntegerField(default=0)
    phone = models.CharField(max_length=14)
    rollno = models.CharField(max_length=10)

    def __str__(self):
        return self.rollno
