#created on 1/6/20

#
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.sessions.models import Session
from .forms import ResumeForm, ProfileUpdateForm
from . import rule_based
import pandas as pd
# Create your views here.
PATH = 'my_app/proposals.csv'
#PATH = 'resolved.txt'
PATH_MENTOR_SKILLS = 'my_app/mentors.csv'
tmp_data=pd.read_csv('my_app/proposals.csv')
proposal_list=[]
for i in tmp_data:
    proposal_list.append(i)
    
    tmp_data.shape
#print(request.user.Profile.name)
#print(request.user.username)
proposal_list = rule_based.wrapper(PATH,PATH_MENTOR_SKILLS)
#print(proposal_list[1][409])

@login_required
def Profile_View(request):
    if request.session.has_key('my_car'):
        if request.user.is_authenticated :        
            return render(request,'my_app/profile.html')
        else:
            return redirect('my_app:login_view')



def Upload_Resume_View(request):
    if request.session.has_key('my_car'): 
        r_form = ResumeForm()
        if request.method == 'POST':
            r_form = ResumeForm(request.POST,
                                request.FILES,
                                instance=request.user.Profile)
            
        
            if r_form.is_valid():
                r_form.save()
                return redirect('my_app:profile')
            else:
                r_form = ResumeForm(instance = request.user.Profile)

        return render(request,'my_app/resume.html',{'r_form':r_form})
    else:
        return redirect('my_app:login_view')

def Proposals_View(request):
    if request.session.has_key('my_car'):
        #from mentorskills import *

        mentorlist=[]
        length = len(proposal_list[0])
        for i in range(0,length):
            name = list(proposal_list[0].items())[i][0]
            uname = request.user.username
            if name == uname:
                #print(name)
                mentorlist=list(proposal_list[0].items())[i][1]
                break
            else:
                mentorlist=['no proposals']
        proposals=[]
        for i in range(0,length):
            name = list(proposal_list[0].items())[i][0]
            uname = request.user.username
            if name == uname:
                for j in mentorlist:
                    temp=[]
                    temp=proposal_list[1][j]
                    proposals.append(temp)
                break
            else:
                proposals:'no proposals'
                
        #print(proposals)
        context = {
            'proposals':proposals,
        }
        #print(list(proposal_list[0].items())[0][1])
        #mentor=list(proposal_list[0].items())[0][0]
        
        return render(request,'my_app/proposals.html',context)
    else:
        return redirect('my_app:login_view')

def Update_Profile_View(request):
    if request.session.has_key('my_car'):
        if request.method == 'POST':
            p_form = ProfileUpdateForm(request.POST, instance=request.user.Profile)
            if p_form.is_valid():
                p_form.save()
                messages.success(request, f'Your account has been updated')
                return redirect('my_app:update_profile')

        else:
            p_form = ProfileUpdateForm(instance=request.user.Profile)

        context = {
            'p_form':p_form,
        }
        
        return render(request,'my_app/update_profile.html',context)
    else:
        return redirect('my_app:login_view')

def Login_View(request):
    if request.session.has_key('my_car'): 
        return redirect('my_app:profile')
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            
            user = form.get_user()
            login(request, user)
            request.session['my_car'] = True
            return redirect('my_app:profile')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/new_login.html',{'form':form})

def Logout_View(request):
    if request.method == 'POST':
        logout(request)
        return redirect('my_app:login_view')


 


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('my_app:login_view')
    else:
        form = UserCreationForm()
    return render(request,'registration/register.html',{'form':form})



