from django import forms
from onlinetest.models import Profile

class ProfileForm(forms.ModelForm):
    # email = 
    class Meta:
        model = Profile
        fields = [
            'phone',
            'rollno'
        ]
    
    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)