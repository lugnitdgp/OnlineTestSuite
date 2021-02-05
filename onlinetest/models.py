from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from tinymce.models import HTMLField
from bs4 import BeautifulSoup


class Question(models.Model):
    title = HTMLField()
    image = models.ImageField(upload_to="question_images/", null=True, blank=True)

    def __str__(self):
        return BeautifulSoup(self.title).get_text()


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
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    rollno = models.CharField(max_length=10)
    image = models.CharField(max_length=200, blank=True)

    # for admin uses
    remarks = models.TextField(help_text="Write remarks after reviewing", blank=True, null=True)
    selected = models.BooleanField(default=False)
    viewed_by = models.ManyToManyField(User, blank=True, related_name="views")

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.full_name


class Config(models.Model):
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    result_release_time = models.BooleanField(default=False, help_text="To make results visible or not")

    def __str__(self):
        return "Project Wide Settings"
