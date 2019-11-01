from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from onlinetest.models import Question
from onlinetest.forms import ProfileForm
from django.http import HttpResponseRedirect


def index(req):
    return render(req, 'onlinetest/index.html')

# @login_required
def Questions(req):
    if req.method == "POST":
        pass
    else:
        questions = Question.objects.all()
        ctx = { 'questions': questions }
        return render(req, 'onlinetest/questions.html', ctx)

def Rules(req):
    return render(req, 'onlinetest/rules.html')

def CreateProfile(req):
    if req.method == "POST":
        form = ProfileForm(req.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('questions/', {})
    else:
        form = ProfileForm()
        return render(req, 'onlinetest/register.html', {'form':form})
