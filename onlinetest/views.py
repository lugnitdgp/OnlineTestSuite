from django.shortcuts import render

# Create your views here.
def index(req):
    return render(req, 'onlinetest/index.html')

def questions(req):
    return render(req, 'onlinetest/questions.html')

def rules(req):
    return render(req, 'onlinetest/rules.html')
