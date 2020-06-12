from django import forms
from django.contrib.auth.models import User
from .models import Mentors

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Mentors
        fields = ['pdfs']

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    full_names = forms.CharField(label=('Name'))
    image = forms.ImageField(label=('Image'),widget=forms.FileInput)
    class Meta:
        model = Mentors
        fields = [ 'full_names', 'emails', 'image']