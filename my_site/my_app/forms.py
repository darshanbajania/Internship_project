# created on 1/6/20

# by Darshan Bajania
#for creating form
from django import forms
from django.contrib.auth.models import User
from .models import Mentors
from cloudinary.forms import CloudinaryFileField

#for uploading resume
class ResumeForm(forms.ModelForm):
    resume = CloudinaryFileField(
        options={
            'folder': 'resume',
            'resource_type': 'raw',
        })

    class Meta:
        model = Mentors
        fields = ['pdfs', 'resume']

#for updating email
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

#for upldating profile properties like profile pic, name email 
class ProfileUpdateForm(forms.ModelForm):
    image = CloudinaryFileField(
        options={
            'folder': 'avatars'
        })
    full_names = forms.CharField(label=('Name'))

    class Meta:
        model = Mentors
        fields = ['full_names', 'emails', 'image']
