from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class Question(models.Model):
    title = models.CharField(max_length=1024)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        str_repr = self.text[:51] + \
            "..." if (len(self.text) >= 52) else self.text
        return str_repr


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_left = models.IntegerField(default=4500) #time in seconds, default 1hour
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    rollno = models.CharField(max_length=10)

    # for admin uses
    remarks = models.TextField(help_text="Write remarks after reviewing", blank=True, null=True)
    selected = models.BooleanField(default=False)
    viewed_by = models.ManyToManyField(User, blank=True, related_name="views")
    selected_for_task_round = models.BooleanField(default=False)
    priority = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], help_text="You can set priority from 0 to 10")

    def __str__(self):
        return self.full_name


class Config(models.Model):
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    result_release_time = models.DateTimeField(default=datetime.now)
    results_list_count = models.IntegerField(default=30)

    def __str__(self):
        return "Project Wide Settings"
