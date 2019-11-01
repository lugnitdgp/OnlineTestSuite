from django import forms
from onlinetest.models import Profile, Answer
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    # fields for user creation
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = [
            'phone',
            'rollno'
        ]

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        #create a user programmatically here
        if commit:
            profile.save()
        return profile

class AnswerForm(forms.ModelForm):
    question_id = forms.IntegerField()
    class Meta:
        model = Answer
        fields = ['text', 'question_id']

    def save(self, user_id, commit=True):
        ans = super(AnswerForm, self).save(commit=False)
        ans.user = User.objects.get(pk=user_id)
        
        if commit:
            ans.save()
        return ans

