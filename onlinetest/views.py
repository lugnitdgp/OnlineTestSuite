from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from onlinetest.models import Question, Answer, Profile, Config
from onlinetest.forms import ProfileForm, AnswerForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.utils import timezone
import os
import csv


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        profile = user
        try:
            player = Profile.objects.get(user=profile)
        except:
            player = Profile(user=profile)
            player.full_name = response.get('name')
            player.image = response.get('picture')
            player.save()


def index(req):
    config = Config.objects.all().first()
    time_left = int(config.start_time.timestamp())
    image = None
    if req.user.is_authenticated:
        if req.user.is_superuser and not Profile.objects.filter(user = req.user).exists():
            Profile(user=req.user, image=req.build_absolute_uri("/static/onlinetest/defavatar.jpeg")).save()
        image = Profile.objects.get(user=req.user).image
        curr_time = timezone.now()
        if curr_time > config.end_time and not req.user.is_staff:
            return redirect('/finish/')
        elif (curr_time > config.start_time and curr_time < config.end_time) or not Profile.objects.get(user=req.user).phone:
            return redirect('/rules/')

    ctx = {}
    if config.result_release_time:
        ctx['release_result'] = True
    if image:
        ctx['image'] = image
    if config.start_time > timezone.now():
        ctx['time_left'] = time_left
        return render(req, 'onlinetest/index.html', ctx)
    elif config.end_time < timezone.now():
        ctx['ended'] = True
        return render(req, 'onlinetest/index.html', ctx)
    ctx['time_left'] = int(config.end_time.timestamp())
    ctx['started'] = True
    return render(req, 'onlinetest/index.html', ctx)


@login_required
def logout_user(req):
    logout(req)
    return redirect('/')


@login_required
def questions(req):
    profile = Profile.objects.get(user=req.user)
    time_left = (Config.objects.all().first().end_time - timezone.now()).total_seconds()

    if timezone.now() < Config.objects.all().first().start_time:
        return redirect('/')
    if time_left <= 0:
        return HttpResponseRedirect('/finish/', {'image': profile.image})
    questions = Question.objects.all()
    answers = Answer.objects.filter(user=req.user)
    # pair up the questions with their corresponding answers
    for question in questions:
        is_answered = answers.filter(question=question).exists()
        if is_answered:
            question.answer = answers.filter(question=question).first().text
        else:
            question.answer = None

    name = profile.full_name
    ctx = {'questions': questions, 'user': name, 'time_left': time_left, 'image': profile.image}
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
                messages.info(req, 'Answer updated successfully {}'.format(qid))
            else:
                answer = Answer(question=question, user=user, text=req.POST['text'])
                answer.save()
                messages.info(req, 'Answer submitted successfully {}'.format(qid))
            if question == Question.objects.all().last():
                return redirect('/questions/#q{}'.format(qid))
            return redirect('/questions/#q{}'.format(qid))
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
            profile = Profile.objects.get(user=user)
            profile.full_name = full_name
            profile.phone = phone
            profile.rollno = rollno
            profile.save()
            return redirect('/questions/')
    else:
        if Profile.objects.filter(user=req.user).exists() and Profile.objects.get(user=req.user).phone:
            return HttpResponseRedirect('/questions/', {})
        ctx = {'user': req.user, 'noprofile': True, 'image': Profile.objects.get(user=req.user).image}
        return render(req, 'onlinetest/rules.html', ctx)


@login_required
def finish(req):
    profile = Profile.objects.get(user=req.user)
    discord_link = Config.objects.all().first().discord_link
    name = profile.full_name
    ctx = {'user': name, 'image': profile.image, 'discord': discord_link}
    return render(req, 'onlinetest/finish.html', ctx)


def results(req):
    image = None
    if req.user.is_authenticated:
        image = Profile.objects.get(user=req.user).image

    ctx = {}
    if image:
        ctx['image'] = image

    config = Config.objects.all().first()
    curr_time = timezone.now()
    if not config.result_release_time:
        ctx['not_declared'] = True
    else:
        profiles = Profile.objects.filter(selected=True)
        profiles = sorted(profiles, key=lambda o: o.full_name)

        ctx['profiles'] = profiles
        ctx['count'] = len(profiles)

    return render(req, 'onlinetest/results.html', ctx)


