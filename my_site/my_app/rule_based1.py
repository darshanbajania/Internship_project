# -*- coding: utf-8 -*-
"""
Created on Thu May 28 21:00:56 2020

@author: Mathew
"""
from gensim.summarization import keywords
import string
import re
import numpy as np
import pandas as pd
#from proptodict import *
#from mentorskills import *
PATH = './media/rule_based/proposals.csv'
#PATH = 'resolved.txt'
PATH_MENTOR_SKILLS = './media/rule_based/mentors.csv'

def read_skills(PATH):
   f = open(PATH)
   l = f.readlines()
   l = [x.rstrip('\n') for x in l]
   arranged = []
   temp =[]
   for i in l:
      if len(i)>50:
         s = i.split(',')[1:]
         
         s = s[:23] + s[-1:]
         temp.append(s)
   k = temp[0]
   keys = []
   for i in k:
      if len(i.split("["))>1:
         keys.append(i.split("[")[1][:-1])
      else:
         keys.append(i)
   data = temp[1:]
   t = []
   for d in data:
      td ={}
      for i in range(len(d)):
         td[keys[i]] = d[i] 
      t.append(td)
   return t

def eliminate_skills(skills):
   keys = list(skills[0].keys())
   for i in range(len(skills)):
      for j in range(len(keys)):
         if skills[i][keys[j]] == 'novice':
            skills[i].pop(keys[j])
   return skills

def Sort_mentors(sub_li): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of  
    # sublist lambda has been used 
    return(sorted(sub_li, key = lambda x: len(x[1])))

def Sort_skills(sub_li): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of  
    # sublist lambda has been used 
    return(sorted(sub_li, key = lambda x: x[0]))


     
def skill_search(texts,skills):
   skillset = []
   for p in texts:#pick up a proposal at a time
      skill_small =[]
      prop = p.lower()
      prop = prop.translate(str.maketrans('', '', string.punctuation))#remove punctuation
      for skill in skills:
         flag = 0 
         key = skill.split(':')[0] # extract true skill name
         vals = skill.split(':')[1].split(',') # extract rules
         for v in vals:
            flag += prop.split(' ').count(v)
#            if v in prop.split(' '):
#               flag+=1
         if flag>=1:
            skill_small.append(key)
         
      skillset.append(skill_small)
   return skillset            

def convert2std(mentor_data_cleaned,skills):
   temp = []
   for i in range(len(mentor_data_cleaned)):
      current = mentor_data_cleaned[i]
      name = current['Full Name']
      skillset = list(current.keys())[2:]
      skill_text = ""
      for s in skillset:
         skill_text += s+' '
#      print("___________________________________")
#      print(skillset)
#      print(skill_search([skill_text.lower()],skills))   
      temp.append([name,skill_search([skill_text.lower()],skills)[0]])
   return temp   
#assigned,proposals= wrapper(PATH,PATH_MENTOR_SKILLS,3)
        
            

def conv2dict(PATH):
#Role : convert proposals tolist of dict
#Input(s) : path to proposals csv
#Output(s) : list of dictionaries
   return_list = []
   f = open('./media/rule_based/skill_dict.txt')
   skills = f.readlines()
   f.close()
   skills = [x[:-1] for x in skills]
   df = pd.read_excel('./media/rule_based/test.xlsx')
#   f = open(PATH,'r',encoding = 'utf-8')
#   proposals = f.readlines()
#   f.close()
   proposals = list(df.Text)
   count = 0
   for prop in proposals:
      words = prop.split(' ')[1:4]
      entry = {'title':'', 'id':'', 'text':'','summary':'','categories':'','svm_categories':''}
      entry['id'] = count
      entry['text'] = prop
      entry['title'] = list(df.Title)[count]
      entry['summary'] = list(df.Sumary)[count] #spelling wrong in excel file 
      proposal_skills = skill_search([prop],skills)
      entry['categories'] = proposal_skills[0]
      count += 1
      return_list.append(entry) 
   return return_list  
 
# def conv2dict(PATH):
#    return_list = []
#    f = open('./media/rule_based/skill_dict.txt')
#    skills = f.readlines()
#    f.close()
#    skills = [x[:-1] for x in skills]
   
#    f = open(PATH,'r',encoding = 'utf-8')
#    proposals = f.readlines()
#    f.close()
#    count = 0
#    for prop in proposals:
#       words = prop.split(' ')[1:4]
#       entry = {'title':'', 'id':'', 'text':'','summary':'','categories':'','svm_categories':''}
#       entry['id'] = count
#       entry['text'] = prop
#       entry['title'] = " ".join(words)
#       proposal_skills = skill_search([prop],skills)
#       entry['categories'] = proposal_skills[0]
#       count += 1
#       return_list.append(entry) 
#    return return_list

def mentor_skills(PATH_MENTOR_SKILLS):
   f = open('./media/rule_based/skill_dict.txt')
   skills = f.readlines()
   f.close()
   skills = [x[:-1] for x in skills]
   
   mentor_data = read_skills(PATH_MENTOR_SKILLS)
   mentor_data_cleaned = eliminate_skills(mentor_data)
   temp = convert2std(mentor_data_cleaned,skills)
   return temp
  #final,list_of_dict =  wrapper(PATH,PATH_MENTOR_SKILLS,list_of_dict,num_proposals) 

def allocate(mentor_data,proposal_data):
   return_list = []
   mentor_data = Sort_mentors(mentor_data)
   num_mentor = len(mentor_data)
   count = -1
   for m in mentor_data:
      
      count += 1
      name = m[0]
      skills = set(m[1])
      num_prop = m[2]
      matches = []
      for proposal in proposal_data:
         ps = set(proposal['categories'])
         score = len(list(skills & ps))/(len(ps) + 1)
         matches.append([score,proposal['id']])
      matches = Sort_skills(matches)
      if num_prop == 'def':
         n = int(len(proposal_data)/(num_mentor-count))
      else:
         n = int(num_prop)
      allocated = matches[-1 * n:]
      allocated = [x[1] for x in allocated]
      temp = []
      for p in proposal_data:
         if p['id'] not in allocated:
            temp.append(p)
      proposal_data = temp
      return_list.append([name,allocated])
   return return_list



#proposal_data = conv2dict(PATH)         
#
#mentor_data = mentor_skills(PATH_MENTOR_SKILLS)
#
#op = allocate(mentor_info,proposal_data)      
#  
#
