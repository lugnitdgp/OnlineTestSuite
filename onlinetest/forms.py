from django import forms
from onlinetest.models import Profile, Answer
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    # fields for user creation
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = [
            'full_name',
            'phone',
            'rollno'
        ]



class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = [
            'text'
        ]

  
