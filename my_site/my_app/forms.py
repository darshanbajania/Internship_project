from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pdfs']

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    name = forms.CharField()
    class Meta:
        model = Profile
        fields = [ 'name','email', 'image']