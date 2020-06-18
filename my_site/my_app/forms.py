from django import forms
from django.contrib.auth.models import User
from .models import Mentors
from cloudinary.forms import CloudinaryFileField

class ResumeForm(forms.ModelForm):
    resume = CloudinaryFileField(
    options = {
        'folder': 'resume',
        'resource_type':'raw',
    })
    class Meta:
        model = Mentors
        fields = ['pdfs','resume']

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    image = CloudinaryFileField(
    options = {
        'folder': 'avatars'
    })
    full_names = forms.CharField(label=('Name'))
    class Meta:
        model = Mentors
        fields = [ 'full_names', 'emails', 'image']