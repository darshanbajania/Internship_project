#created on 1/6/20

#formatted on 5/6/20
#by Darshan Bajania

#importing required libraries
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Mentors, Proposal
from django.contrib.sessions.models import Session
from .forms import ResumeForm, ProfileUpdateForm
from . import rule_based,rule_based1,all_functions
from django.urls import reverse
from urllib.parse import urlencode

import slate3k as slate

import pandas as pd

from PyPDF2 import PdfFileReader, PdfFileWriter
 
#for text extraction 

# with open('my_app/resume_list.pdf', 'rb') as f:
#     extracted_text = slate.PDF(f)
# text=(str(extracted_text[6]))
# #print(str(extracted_text[6]))
# # pdf_miner =  [x for x in extracted_text[0].split("\n") if x != ""]

# text=str(text.split('\n'))
# text=text.split('][')
# #print(text)
# extracted_skills=all_functions.skill_extract(text)[0]
# print(extracted_skills)
# # for skills in extracted_skills:
#     print(skills)
# with open('my_app/demo.txt', 'w') as f:
#     f.write(str(pdf_miner))
#     f.close()
# file_path = 'my_app/test_sample.pdf'




# pdf = PdfFileReader(file_path)
 
# with open('my_app/demo.txt', 'w') as f:
#     for page_num in range(pdf.numPages):
#         # print('Page: {0}'.format(page_num))
#         pageObj = pdf.getPage(page_num)
 
#         try: 
#             txt = pageObj.extractText()
#             print(''.center(100, '-'))
#         except:
#             pass
#         else:
#             f.write('Page {0}\n'.format(page_num+1))
#             f.write(''.center(100, '-'))
#             f.write(txt)
#     f.close()


# Create your views here.
print("yes, its working")

# first argument for Wrapper function
PATH = './media/rule_based/proposals.csv'
#Second argument for wrapper function
PATH_MENTOR_SKILLS = './media/rule_based/mentors.csv'
#reading proposals to use in proposals view
tmp_data=pd.read_csv('./media/rule_based/proposals.csv')

new_list = rule_based1.conv2dict(PATH)
new_mentor_skills = rule_based1.mentor_skills(PATH_MENTOR_SKILLS)
#print(new_list[5])   
#pasing paths as arguments and getting back mentors, proposals and their skills 
[proposal_list,propsl,skills] = rule_based.wrapper(PATH,PATH_MENTOR_SKILLS)


value=0


@login_required

#Shows profile of the user
def Profile_View(request):
    if request.session.has_key('is_logged_in'):#checking for sessions
        if request.user.is_authenticated :
            if request.user.username == "admin":# check wheter the use is admin or not
                return redirect('my_app:admin_profile')#if admin redirect to admin profile

            user_skills=[]
            status_list = Mentors.objects.get(user=request.user)
            status_list.name=request.user.username
            status_list.save()
            #print(status_list.name)
            user_count=Mentors.objects.all().count()#counts all users in Mentors model
            #loop for getting all the usernames
            for i in range(1,user_count+1):
                user=Mentors.objects.filter(name = request.user.username).first()
                #print(user.user)
                if user != None:
                    b=user.name#getting the username
                #print(request.user.username)
                    p=str(b)
                    if(p==request.user.username):#checking if current user name matches with the mentors in database
                        #print(user.user)
                        #print(user.name)
                        user_skills=eval(user.skills)
                        #print(user.skill_level)
                        user_skills_level = eval(user.skill_level)                        
                        
                        if user.name == "1":                   
                            p=user
                            p.name=request.user.username
                            #print(p.name)
                            p.save()#saving the username as name
            
            #print(user_skills_level.keys())
            level_count=3
            context = {
                #'total_skills':total_skills,#total skills of current mentor
                'user_skills':user_skills,
                'user_skills_level':user_skills_level,
                'level_count':level_count,
            }
        return render(request,'my_app/profile.html',context)
    else:#if session is not there redirect to login page  
        return redirect('my_app:login_view')

#Shows upload resume page
def Upload_Resume_View(request):
    if request.session.has_key('is_logged_in'):#checking for sessions
        r_form = ResumeForm()#creating instance for resume upload form
        if request.method == 'POST':#if method is post than fill the form with passed details
            r_form = ResumeForm(request.POST,
                                request.FILES,
                                instance=request.user.Profile)        
            if r_form.is_valid():#if form is valid then save it and return to profile
                r_form.save()
                return redirect('my_app:profile')
            else:#else return to the same page
                r_form = ResumeForm(instance = request.user.Profile)
        return render(request,'my_app/resume.html',{'r_form':r_form})
    else:#if sessions is not there then redirect to login page
        return redirect('my_app:login_view')

# Shows proposals for individual mentor
def Proposals_View(request):
    if request.session.has_key('is_logged_in'):#checking for sessions
        mentor_proposals=Proposal.objects.all()
        if request.method == "POST":
            proposal_number=request.POST.get('proposal')
            base_url = reverse('my_app:full_proposal')  # getting the url for displaying full proposal
            query_string =  urlencode({'category': proposal_number}) #creating a string of dictionary
            url = '{}?{}'.format(base_url, query_string)  # passing the base_url and query from this page to url
         
            #print(proposal_number)
            return redirect(url)# redirecting to the full proposal page

        c=0  
        count = 0
        user=Mentors.objects.filter(name = request.user.username).first()
        b=user.user#getting the username)
        p=str(b)
        if(p==request.user.username):#checking if current user name matches with the mentors in database           
            if user.prop_no == "def" :
                test = list(user.propsl_list.split(' '))
                c=len(test)
                count=0
                bsc=Proposal.objects.filter(ids="abc") # initialising with None
            else:
                c=int(user.prop_no)#it is the no. of proposals      
                count = 0
                bsc=Proposal.objects.filter(ids="asd") # initializing with None
            for ele in list(user.propsl_list.split(' ')):#gettting the no. of proposals assigned to current mentor
                if count < c:
                    mentor_proposals=Proposal.objects.filter(ids=str(ele))#filtering the proposals mentioned in proposal_list
                    bsc=bsc|mentor_proposals # cascading the proposals in a query list

        #print(bsc)       
        pagin = Paginator(bsc, 12)#create a paginator having 12 items per page 
        page_number = request.GET.get('page')#get te value of next page
        #print(pagin.page(1))
        paginator = pagin.get_page(page_number)#get the contents of next page
        
        context = {
            'paginator':paginator,#contents of page
        }     
        return render(request,'my_app/proposals.html',context)
    else:#if sessions are not there then redirect to login page
        return redirect('my_app:login_view')

#Shows page for update user profile
def Update_Profile_View(request):
    if request.session.has_key('is_logged_in'):#checking for sessions
        if request.method == 'POST':#for creating an instance of profile update form with passed details
            p_form = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                         instance=request.user.Profile)
            #print(p_form)
            if p_form.is_valid():#if form is valid then save it
                p_form.save()#and give a success messsage
                messages.success(request, f'Your account has been updated')
                return redirect('my_app:update_profile')
        else:#create an instance of form with current details
            p_form = ProfileUpdateForm(instance=request.user.Profile)
            print(p_form)
        context = {
            'p_form':p_form,#passing the form to the update profile page
        }        
        return render(request,'my_app/update_profile.html',context)
    else:#if sessions are not there redirect to login page
        return redirect('my_app:login_view')

#Shows login page
def Login_View(request):
    if request.session.has_key('is_logged_in'):#if session is there redirect to profile page 
        return redirect('my_app:profile')
    if request.method == 'POST':#authanticate user using login page
        
        username = request.POST.get('username')#getting the username of current user
        password = request.POST.get('password')#getting the password of current user
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)#authenticating current user

        if user is not None:# A backend authenticated the credentials
            login(request, user)#logging in the current user
            request.session['is_logged_in'] = True#make the session true after logging in
            if (username == 'admin'):#if user is admin redirect it to admin_page
                return redirect('my_app:admin_page')
            else:
                return redirect('my_app:profile')#else to the user profile

        else:
            # No backend authenticated the credentials
            return render(request, 'registration/new_login.html')

    return render(request, 'registration/new_login.html')

#shows logout page //not used
def Logout_View(request):
        logout(request)
        return redirect('my_app:login_view')

#Shows all the proposals with pagination 
def Total_Proposal_View(request):
    if request.session.has_key('is_logged_in'):#checking for sessions

        if request.method == "POST":
            proposal_number=request.POST.get('proposal')
            base_url = reverse('my_app:full_proposal_admin') # getting the url for displaying full proposal
            query_string =  urlencode({'category': proposal_number}) #creating a string of dictionary
            url = '{}?{}'.format(base_url, query_string)  # passing the base_url and query from this page to url
         
            #print(proposal_number)
            return redirect(url)

        all_proposals=Proposal.objects.filter(ids='ds') #initializing query set with None
    
        for i in range(0,495): 
            propsal_temp = Proposal.objects.filter(ids=str(i))# filtering all the proposals
            if propsal_temp.first()!=None:
                #print(propsal_temp.first().ids)
                all_proposals=all_proposals|propsal_temp #adding all proposals query set

        # all_proposals=Proposal.objects.all()
       #print(all_proposals)
        pagin = Paginator(all_proposals, 12)#create a paginator having 12 items per page
        # page1 = pagin.page(1) 
        page_number = request.GET.get('page')#get the page number of next page
        #print(page_number)
        paginator = pagin.get_page(page_number)#get the contents of next page
        #print(paginator)
        form={
            'paginator':paginator,#contents of next page
        }
        return render(request,'my_app/proposal_admin.html',form)
    else:# if there are no sessions then redirect to login page
        return redirect('my_app:login_view')

#shows password reset page //not used
def password_Reset_View(request):
    if request.session.has_key('is_logged_in'):
        form = PasswordResetForm()
        return render(request,'registration/password_reset_for.html',{'form':form})
    else:
        return redirect('my_app:login_view')

#Shows page to register a new user
def register_view(request):
    if request.session.has_key('is_logged_in'):#if sessions are there redirect to profile page 
        return redirect('my_app:profile')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)#form for creating new user 
        if form.is_valid():#if valid then create new user and redirect to login page
            form.save()
            return redirect('my_app:login_view')
    else:#if form is not correct redirect to the the reggister page with a form
        form = UserCreationForm()
    return render(request,'registration/register.html',{'form':form})

#shows page for admin
def Admin_view(request):
    if request.session.has_key('is_logged_in'):
        
        mentors_list=Mentors.objects.filter(name='ds')#initializing query set with None
        length = len(skills)
        for i in range(0,length):
            name = list(proposal_list.items())[i][0]#list having name of Mentor 
            new_mentor_name=all_functions.convert_space_to_us(name)#replacing space with underscore            
            user=Mentors.objects.filter(name = new_mentor_name)#filtering the name 
            if user.first()!=None:
                print(user.first().name)
                mentors_list=mentors_list|user#adding the name of the user to the mentor list

        # all_functions.remove_comma_from_proposal()

        if request.user.is_anonymous:#if user is anonymous then redirect to login page
            return redirect('my_app:login_view') 
        if request.method == "POST":
            for i in mentors_list:# after allocate proposals is clicked
                mentor = i.name # taking out each name
                new_prop_val = request.POST.get(mentor)# getting proposal value from the form 
                #new_prop_val=int(252/19)
                i.prop_no = new_prop_val
                i.save()#saving the proposal no. for each and every user
            all_functions.store_allocated_proposals()# calling the function to 
                                                    #store proposal list in the database for each mentor
            all_functions.assign_mentor_to_proposals()#this function assigns 
                                                      #mentor name to each and every proposal                      
        print("success")
        context = {'prods': mentors_list }#passing the mentors list to the admin page
        return render(request, 'my_app/admin_page.html',context)
    else:
        return redirect('my_app:login_view')

#Shows admin profile page
def Admin_profile_view(request):
    if request.session.has_key('is_logged_in'):
        total_skills=[]
        length = len(skills)
        for i in range(0,length):
            name = list(proposal_list.items())[i][0]
            uname = request.user.username
            #print(name)
            #print(uname)
            new_length = len(skills[i][1])
            #print(new_length)
            if name == uname:
                for j in range(0,new_length):
                    temp=[]
                    #print(j)
                    temp=skills[i][1][j]
                    #print(temp)
                    total_skills.append(temp)
                    break
        #print(total_skills)
        #user=Mentors.objects.filter(user=request.user.username)
        return render(request, 'my_app/admin_profile.html')
    else:
        return redirect('my_app:login_view')

#shows admin profile page
def Admin_Update_Profile_view(request):
    if request.session.has_key('is_logged_in'):#checking for sessions
        if request.method == 'POST':#for creating an instance of profile update form with passed details
            p_form = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                         instance=request.user.Profile)
            #print(p_form)
            if p_form.is_valid():#if form is valid then save it
                p_form.save()#and give a success messsage
                messages.success(request, f'Your account has been updated')
                return redirect('my_app:admin_update_profile')
        else:#create an instance of form with current details
            p_form = ProfileUpdateForm(instance=request.user.Profile)
            print(p_form)
        context = {
            'p_form':p_form,#passing the form to the update profile page
        } 
        return render(request, 'my_app/admin_update_profile.html',context)
    else:
        return redirect('my_app:login_view')


#To display entire proposals for mentor
def Full_Proposal_view(request):
    if request.session.has_key('is_logged_in'):
        category_id = request.GET.get('category')#after getting the category value from 
        proposalss=Proposal.objects.filter(ids=str(category_id)).first()#filtering the particular proposal
        #print("hello",proposalss) 
        context={
            'proposal':proposalss
        }#passing the proposal to the next page
        return render(request,'my_app/full_proposal.html',context)
    else:
        return redirect('my_app:login_view')
# to display entire proposals for admin
def Full_Proposal_Admin_view(request):
    if request.session.has_key('is_logged_in'):
        category_id = request.GET.get('category') #after getting the category value from 
        proposalss=Proposal.objects.filter(ids=str(category_id)).first()#filtering the particular proposal
        #print("hello",proposalss) 
        context={
            'proposal':proposalss
        }#passing the proposal to the next page
        return render(request,'my_app/full_proposal_admin.html',context)
    else:
        return redirect('my_app:login_view')

#To update skills
def Update_Skill_view(request):
    if request.session.has_key('is_logged_in'):

        user_count=Mentors.objects.all().count()#counts all users in Mentors model
        #loop for getting all the usernames

        user=Mentors.objects.filter(name = request.user.username).first()
        #print(user.user)
        if user != None:
            b=user.name#getting the username
        #print(request.user.username)
            p=str(b)
            if(p==request.user.username):#checking if current user name matches with the mentors in database
                #print(user.user)
                #print(user.name)
                user_skills=eval(user.skills)
                user_skills_level=eval(user.skill_level)
                if request.method == "POST":
                    
                    user_keys=user_skills_level.keys()
                    #print(user_keys)
                    for i in user_keys:
                        variab=str(i)
                        form_data=request.POST.get(variab)
                        if form_data!=None:
                            #print(variab,user_skills_level[variab])
                            user_skills_level[variab]=int(form_data)
                            
                            #print(variab,user_skills_level[variab])
                            user.skill_level=str(user_skills_level)
                            user.save()
                            
        values=0
        #print(user_skills_level)
        context = {
                #'total_skills':total_skills,#total skills of current mentor
                'user_skills':user_skills,
                'user_skills_level':user_skills_level,
                'values':values,
            }
        return render(request,'my_app/update_skills.html',context)
    else:
        return redirect('my_app:login_view')

#to show extracted skills
# def Extracted_Skills_view(request):
#     if request.session.has_key('is_logged_in'):

#         user_count=Mentors.objects.all().count()#counts all users in Mentors model
#         #loop for getting all the usernames

#         user=Mentors.objects.filter(name = request.user.username).first()
#         #print(user.user)
#         if user != None:
#             b=user.name#getting the username
#         #print(request.user.username)
#             p=str(b)
#             if(p==request.user.username):#checking if current user name matches with the mentors in database
#                 #print(user.user)
#                 #print(user.name)
#                 with open('.'+user.pdfs.url, 'rb') as f:
#                     extracted_text = slate.PDF(f)
                
#                 # pdf_miner =  [x for x in extracted_text[0].split("\n") if x != ""]
#                 # print(pdf_miner)
#                 text=str(extracted_text)
#                 text=text.split('][')
#                 print(text)
#                 extracted_skills=all_functions.skill_extract(text)[0]
#                 print(extracted_skills)
#                 extracted_skills_list=extracted_skills
#                 # for p in pdf_miner:
#                 #     c=p.lower()
                        
#                 #     if "skills" in c:
#                 #         skills=c.split('skills:-')
                        
#                 #         skills=skills[1].split(', ')
                        
#                 #         extracted_skills_list=eval(str(skills))
#                 #         for j in extracted_skills_list:
#                 #            print(j)
#         context={
#             'skills':extracted_skills_list,
#         }
#         return render(request,'my_app/extracted_skills.html',context)
#     else:
#         return redirect('my_app:login_view')