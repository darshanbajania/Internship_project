# -*- coding: utf-8 -*-
"""
Created on Thu May 28 21:00:56 2020

@author: Mathew
"""
from gensim.summarization import keywords
import string
import re
import numpy as np
#from mentorskills import *
PATH = 'my_app/proposals.csv'
#PATH = 'resolved.txt'
PATH_MENTOR_SKILLS = 'my_app/mentors.csv'

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

def get_data(PATH):
   f = open(PATH,'r',encoding="utf-8")
   props = f.readlines()
   f.close()
   f = open('my_app/skill_dict.txt')
   skills = f.readlines()
   f.close()
   skills = [x[:-1] for x in skills]
   return props,skills
     
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
def match_proposals(converted,proposal_skills,matches):
   return_list = []
   for i in converted:#pick a mentor first
      n = i[0]
      #print(n)
      s = set(i[1]) # mentor's skills
      matched_val = []
      for j in range(len(proposal_skills)):
         ps = proposal_skills[j] #skills of a selected proposal
         ps = set(ps)
         common = list(s & ps)
         if len(common)>=0:
            matched_val.append(len(common))#no. of similarities
            #print(j,common,len(common))
      res = sorted(range(len(matched_val)), key = lambda sub: matched_val[sub])[-matches:]
      return_list.append([n,res])
   return return_list
         

#assigned,proposals= wrapper(PATH,PATH_MENTOR_SKILLS,3)
def alt_match(mentor_skills,proposal_skills,l):
   return_dict = {}
   temp = []
   for i in range(len(proposal_skills)):
      temp.append([proposal_skills[i],i])
   proposal_skills = temp
   del temp
   #print(proposal_skills)
   num_mentor = len(mentor_skills)
   prop_per_ment = int(len(proposal_skills)/num_mentor)
   mentor_skills = Sort_mentors(mentor_skills)

   m_c = -1
   for m in mentor_skills: # pick a mentor
      m_c += 1
      name = m[0]
      m_s = set(m[1]) #mentor's skills
      matches = []
      for j in range(len(proposal_skills)):
         p_s = set(proposal_skills[j][0])
         common_s = list(m_s & p_s)
         matches.append([len(common_s)/(len(p_s)+1),proposal_skills[j][1]])
      #matches now hold the relevance wrt to each proposal + global index
      matches = Sort_skills(matches)
      if l[m_c] == -1:
         prop_per_ment = int(len(proposal_skills)/(num_mentor-m_c))
      else:
         prop_per_ment = int(l[m_c])
      allocated = matches[-1*prop_per_ment:]
      allocated = [x[1] for x in allocated]
      return_dict[name] = allocated
      for a in allocated:
         temp =[]
         for j in range(len(proposal_skills)):
            if proposal_skills[j][1] != a:
               temp.append(proposal_skills[j])
         proposal_skills = temp
   keys = list(return_dict.keys())[::-1]
   for i in range(len(proposal_skills)):
      return_dict[keys[i]].append(proposal_skills.pop(0)[1])
   #print(proposal_skills)
   return return_dict        
            
def wrapper(PATH,PATH_MENTOR_SKILLS,l=[-1 for x in range(19)]):       
   proposals,skills = get_data(PATH)
   proposal_skills = skill_search(proposals,skills)
   mentor_data = read_skills(PATH_MENTOR_SKILLS)
   mentor_data_cleaned = eliminate_skills(mentor_data)
   temp = convert2std(mentor_data_cleaned,skills)
   print(temp)
   #final = match_proposals(temp,proposal_skills,results)
   final = alt_match(temp,proposal_skills,l)
   return final,proposals      
         
#l = [-1 for x in range(19)]
#l[3] = 22   
#final,proposals =  wrapper(PATH,PATH_MENTOR_SKILLS,l)

