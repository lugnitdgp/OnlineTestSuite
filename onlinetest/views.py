from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from onlinetest.models import Question, Profile
from onlinetest.forms import ProfileForm, AnswerForm
from django.http import HttpResponseRedirect, HttpResponse


def index(req):
    return render(req, 'onlinetest/index.html')

# @login_required
def Questions(req):
    if req.method == "POST":
        ans_form = AnswerForm(req.POST)
        if ans_form.is_valid():
            ans_form.save(user_id=req.user.pk)
        
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

def UpdateTime(req):
    if req.method == "POST":
        t_left = int(req.POST['time_left'])
        profile = Profile.objects.get(user=req.user)
        if t_left <= 0:
            profile.time_left = 0
            profile.save()
            return HttpResponse(status=200)

        if t_left < profile.time_left:
            # possibly valid
            profile.time_left = t_left
            profile.save()
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=406) # 406-NotAcceptable
    else:
        return None



