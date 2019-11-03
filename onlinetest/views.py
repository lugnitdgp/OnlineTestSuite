from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from onlinetest.models import Question, Answer, Profile
from onlinetest.forms import ProfileForm, AnswerForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout


def index(req):
    if req.user.is_authenticated:
        return redirect('/rules/')
    return render(req, 'onlinetest/index.html')

@login_required
def logout_user(req):
    logout(req)
    return redirect('/')

@login_required
def questions(req):
    profile = Profile.objects.get(user=req.user)
    if profile.time_left <= 0:
        return HttpResponseRedirect('/finish/', {})
    questions = Question.objects.all()
    answers = Answer.objects.filter(user=req.user)
    # pair up the questions with their corresponding answers
    for question in questions:
        is_answered = answers.filter(question=question).exists()
        if is_answered:
            question.answer = answers.filter(question=question).first().text
        else:
            question.answer = None

    time_left = profile.time_left
    ctx = { 'questions': questions, 'user': req.user , 'time_left': time_left}
    return render(req, 'onlinetest/questions.html', ctx)

@login_required
def answers(req, qid):
    if req.method == 'POST':
        form = AnswerForm(req.POST)
        if form.is_valid:
            question = Question.objects.get(id=qid)
            user = User.objects.get(id=req.user.id)
            already_submitted = Answer.objects.filter(question=question, user=user).exists()
            if already_submitted:
                answer = Answer.objects.filter(question=question, user=user).first()
                answer.text = req.POST['text']
                answer.save()
                messages.info(req, 'Your answer for Question {} has been updated.'.format(qid))
            else:
                answer = Answer(question=question, user=user, text=req.POST['text'])
                answer.save()
                messages.info(req, 'Successfully submitted answer for Question {}.'.format(qid))
            return redirect('/questions/#q{}'.format(qid + 1))
        else:
            messages.info(req, 'Please supply a valid answer.')
            return redirect('/questions/#q{}'.format(qid))
    else:
        return HttpResponse(status=404)

@login_required
def rules(req):
    if req.method == 'POST':
        form = ProfileForm(req.POST)
        if form.is_valid:
            full_name = req.POST['full_name']
            phone = req.POST['phone']
            rollno = req.POST['rollno']
            user = User.objects.get(id=req.user.id)
            profile = Profile(user=user, full_name=full_name, phone=phone, rollno=rollno)
            profile.save()
            return redirect('/questions/')
    else:
        if Profile.objects.filter(user=req.user).exists():
            return HttpResponseRedirect('/questions/',{})   
        ctx = {'user': req.user, 'noprofile': True}
        return render(req, 'onlinetest/rules.html', ctx)

def CreateProfile(req):
    if req.method == "POST":
        form = ProfileForm(req.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/questions/', {})
    else:
        form = ProfileForm()
        return render(req, 'onlinetest/register.html', {'form':form})

@csrf_exempt
def UpdateTime(req):
    if req.method == "POST":
        print(req.POST)
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

@login_required
def finish(req):
    ctx = { 'user': req.user }
    return render(req, 'onlinetest/finish.html', ctx)
