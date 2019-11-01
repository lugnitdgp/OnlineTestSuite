from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from onlinetest.models import Question

# Create your views here.
def index(req):
    return render(req, 'onlinetest/index.html')

# @login_required
def Questions(req):
    if req.method == "POST":
        pass
    else:
        return render(req, 'onlinetest/questions.html')

def Rules(req):
    return render(req, 'onlinetest/rules.html')

def CreateProfile(req):
    if req.method == "POST":
        form = 