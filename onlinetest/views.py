from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from onlinetest.models import Question


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
        form = 