#created on 8/06/2020
#by Bajania Darshan Kumar


# importing required modules and files
from .models import Mentors,Proposal
from . import rule_based1
import pandas as pd
import pickle
import string


PATH = './media/rule_based/proposals.csv'

PATH_MENTOR_SKILLS = './media/rule_based/mentors.csv'

tmp_data=pd.read_csv('./media/rule_based/proposals.csv')
new_list = rule_based1.conv2dict(PATH)
#print(new_list)
new_mentor_skills = rule_based1.mentor_skills(PATH_MENTOR_SKILLS)



# to convert name with space to to name with underscore
def convert_space_to_us(user_name):
    temp_name=""
    for letter in user_name:
        if letter ==" ":
            letter="_"
        temp_name+=letter
    return temp_name






# to convert name with underscore to to name with space
def convert_us_to_space(user_name):
    temp_name=""
    for letter in user_name:
        if letter =="_":
            letter=" "
        temp_name+=letter
    return temp_name





# for allocating mentors skills
def allocate_proposals_mentor():
    final_allocation_list=[]
    #print("new_mentor_skills:")
    new_mentor_skills = rule_based1.mentor_skills(PATH_MENTOR_SKILLS)
    #print(new_mentor_skills)

    final_allocation_list=new_mentor_skills
    #print(final_allocation_list)
    length_of_skillss = len(new_mentor_skills)
    #print(length_of_skillss)
    for j in range(0,length_of_skillss):
        name=new_mentor_skills[j][0]
        new_mentor_name=convert_space_to_us(name) 
        user=Mentors.objects.filter(name = new_mentor_name)
        if user.first()!=None:
            user_objects=user.first()
            #print(user_objects.name)
            #print(user_objects.prop_no)
            final_allocation_list[j].append(user_objects.prop_no)
    #print(final_allocation_list)  
    skills_allocated = rule_based1.allocate(final_allocation_list,new_list)
    #print(skills_allocated)
    return skills_allocated





# for storing the proposal no. in the database of mentor
def store_allocated_proposals():
    length_of_skills = len(new_mentor_skills)
    allocated_skills=allocate_proposals_mentor()
    #print("hello")
    #print(allocated_skills)
    for j in range(0,length_of_skills):
        name=new_mentor_skills[j][0]
        new_mentor_name=convert_space_to_us(name)
        user=Mentors.objects.filter(name = new_mentor_name)
        if user.first()!=None:
            user_objects=user.first()
            h=user_objects.prop_no
            for m in range(0,len(allocated_skills)):
                
                new_mentor_name=allocated_skills[m][0]
                new_mentor_names=convert_space_to_us(new_mentor_name)
                #print(new_mentor_name)  
                if user_objects.name ==new_mentor_names: 
                    #print(new_mentor_names)
                    #print(user_objects.name)
                    #print(user_objects.propsl_list)
                    #print(skills_allocated[m][1])
                    names = allocated_skills[m][1]#getting no. of proposals of second mentor
                    str1 = ""
                    count = 0
                    if h != None:
                        #print(names)
                        for ele in names:#gettting the no. of proposals assigned to current mentor                            
                            if h=='def':
                                if str1 == "":
                                    str1=str(ele)
                                else:    
                                    str1=str1+ " " +str(ele)
                            else:    
                                if count < int(h):
                                    if count == 0:
                                        str1=str(ele)
                                    else:
                                        str1 =str1+ " " + str(ele)
                                count +=1
                        #print(str1)
                        
                        user_objects.propsl_list=str1#assigning proposal no to current user
                        user_objects.save()
                        print(user_objects.name)
                        print(user_objects.propsl_list) 
                        
    return     

#another code fo allocating proposals
# def store_allocated_proposals2():
    # length_of_proposallist=len(proposal_list)
    # for item in range(0,length_of_proposallist):
    #     new_name = list(proposal_list.items())[item][0]
    #     new_mentor_name=""
    #     for d in new_name:
    #         for j in d:
    #             if j ==" ":
    #                 j="_"
    #             new_mentor_name+=j
    #     if i.name == new_mentor_name:
    #         #print(new_mentor_name)
    #         name = list(proposal_list.items())[item][1]#getting no. of proposals of second mentor
    #         str1 = ""
    #         count = 0
    #         if h != None:
    #             for ele in name:#gettting the no. of proposals assigned to current mentor
    #                 if h=='def':
    #                     str1='def'
    #                 else:    
    #                     if count < int(h):
    #                         if count == 0:
    #                             str1=str(ele)
    #                         else:
    #                             str1 =str1+ " " + str(ele)
    #                     count +=1
    #             listToStr = ' '.join([str(elem) for elem in name])
    #             i.propsl_list=str1#assigning proposal no to current user
    #             #print(i.propsl_list)
    #             i.save()
    #             #print(i)
    #             #print(i.propsl_list)








#for assigninig new values into Proposals model
def add_new_feild_proposal():
    for k in range(0,253):
        propsal_temp = Proposal.objects.filter(ids=str(k))
        temp_var=""
        for each_category in new_list[k]['categories']:
            if temp_var =="":
                temp_var = each_category
            else:    
                temp_var=temp_var+", "+each_category
        demo=propsal_temp.first()
        demo.category=temp_var
        demo.save()

        print(demo.category)
    

#for removing comma from avm categories
def remove_comma_from_proposal():
    for k in range(0,253):
        propsal_temp = Proposal.objects.filter(ids=str(k))
        demo=propsal_temp.first()
        value=""
        temp_var=''
        if demo.svm_categories !=temp_var:
            if demo.svm_categories[0] == ',':
        
                value=demo.svm_categories[2:]
                demo.svm_categories = value
                demo.save()
                print(demo.svm_categories)
    







#for creating new proposals
def create_new_proposals():
    length_of_proposals = len(new_list)
    for j in range(236,length_of_proposals):
        propsls=Proposal()
        propsls.title = new_list[j]['title']
        propsls.ids = str(new_list[j]['id'])
        propsls.text = str(new_list[j]['text'])
        propsls.svm_categories = str(new_list[j]['categories'])
        propsls.summary = new_list[j]['summary']
        propsls.save()




#for predicting using svm models
# def svm_predicting_models():
    # with open('my_app/svm_machine_learning.pkl', 'rb') as file:
    #     pickle_model = pickle.load(file)
    
    # p=pickle_model.predict(new_list)
    # print(p)

#for inserting categories to proposals
# def insert_proposal_categories():

#     with open('./media/svm_models/svm_android.pkl', 'rb') as file:
#         pickle_model = pickle.load(file)
    
#     #p=pickle_model.predict(['robot'])
#     # print(p)

#     for k in range(0,253):
#         propsal_temp = Proposal.objects.filter(ids=str(k))
        
#         new_text=[]
#         temp=""
#         new_text.append(new_list[k]['text'])
#     #     temp="Summary will be displayed here"
#         # print(new_text)
#         p=pickle_model.predict(new_text)
#         print(p[0])
#         if p[0]== 1:
#             temp=", Android App"
#         else:
#             temp=""
#         # for m in range(0,len(new_list[k]['categories'])):
#         #     if m==0:
#         #         temp = new_list[k]['categories'][0]
#         #     else:
#         #         temp=temp+', '+new_list[k]['categories'][m]
#         demo=propsal_temp.first()
#         temp2 = demo.svm_categories
#         temp2=temp2+temp
#         demo.svm_categories = temp2
#         demo.save()
#         print(k)
#         print(demo.svm_categories)
#         #proposal_temp.first().svm_categories=new_list[j]['categories']


#To add mentor assigned to Proposals
def assign_mentor_to_proposals():
    length_of_skills = len(new_mentor_skills)
    
    for j in range(0,length_of_skills):
        name=new_mentor_skills[j][0]
        new_mentor_name=""
        for d in name:
            
            for i in d:
                if i ==" ":
                    i="_"
                new_mentor_name+=i
        user=Mentors.objects.filter(name = new_mentor_name)
        if user.first()!=None:
            user_objects=user.first()
            test_var = list(user_objects.propsl_list.split(' '))
            for i in test_var:
                if i == '-1':
                    for k in range(0, 253):
                        prop_temp = Proposal.objects.filter(ids=k)
                        prop_temp_vairable = prop_temp.first()
                        if prop_temp_vairable.mentor_assigned == user_objects.name:
                            prop_temp_vairable.mentor_assigned = 'No Mentor Assigned'
                            prop_temp_vairable.save()
                        #print(prop_temp_vairable.mentor_assigned)
                else:
                    prop_var = Proposal.objects.filter(ids=i)
                    prop_variable=prop_var.first()
                    prop_variable.mentor_assigned = user_objects.name
                    prop_variable.save()
                    #print(user_objects.name)
                    #print(prop_variable.mentor_assigned)


           
            #print(test_var)



def skill_extract(texts):
    f = open('./media/rule_based/skill_dict.txt')
    skills = f.readlines()
    f.close()
    skills = [x[:-1] for x in skills]
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






#for storing mentor skills of each mentor
def store_mentor_skills():
    length_of_skills = len(new_mentor_skills)
    
    for j in range(0,length_of_skills):
        name=new_mentor_skills[j][0]
        new_mentor_name=""
        for d in name:
            
            for i in d:
                if i ==" ":
                    i="_"
                new_mentor_name+=i
        user=Mentors.objects.filter(name = new_mentor_name)
        if user.first()!=None:
            user_objects=user.first()
            user_objects.skills=str(new_mentor_skills[j][1])
            user_objects.save()
            print(user_objects.skills)



#function for replacing a category
def replace_category():
    no_values=['']
    for k in range(0,253    ):
        propsal_temp = Proposal.objects.filter(ids=str(k))
        new_temp=[]
        demo=propsal_temp.first()
        temp=demo.svm_categories
        new_temp=list(temp.split(", "))
        count=0
        for i in new_temp:
            if i == 'Embedded Systems':
                new_temp[count]='Embedded Systems'
            elif i == 'Iot':
                new_temp[count]='IOT'
            elif i == 'Machine Learning':
                new_temp[count]='Machine Learning'
            elif i == 'Web Designing':
                new_temp[count]='Web Designing'
            elif i == 'Image Processing':
                new_temp[count]='Image Processing'
            elif i == 'Robotics':
                new_temp[count]='Robotics'
            elif i == 'Sensors':
                new_temp[count]='Sensors'
            count+=1

        print(new_temp)








#for printing distribution
def show_distribution():

    count_e_s=0
    count_iot=0
    count_ml=0
    count_w_d=0
    count_i_p=0
    count_n_c=0
    count_r=0
    count_s=0
    count_a=0
    no_categ=[]
    no_values=['']
    for k in range(0,253):
        propsal_temp = Proposal.objects.filter(ids=str(k))

        demo=propsal_temp.first()
        temp=demo.svm_categories
        new_temp=list(temp.split(", "))
        if new_temp== no_values:
            count_n_c+=1
            no_categ.append(new_temp)
        
        for i in new_temp:
            if i == 'Embedded Systems':
                count_e_s+=1
            elif i == 'IOT':
                count_iot+=1
            elif i == 'Machine Learning':
                count_ml+=1
            elif i == 'Web Designing':
                count_w_d+=1    
            elif i == 'Image Processing':
                count_i_p+=1
            elif i == 'Robotics':
                count_r+=1
            elif i == 'Sensors':
                count_s+=1
            elif i == 'Android App':
                count_a+=1

        print(k)
        print(new_temp)
    print("Embedded Systems, IOT, Machine Learning, Web Designing, Image Processing, Robotics, Sensors, Android App, no categories\n",
        "  ",count_e_s,
        "         ",count_iot,
        "      ",count_ml,    
        "              ",count_w_d,
        "           ",count_i_p,
        "         ",count_r,
        "              ",count_s,
        "         ",count_a,
        "            ",count_n_c)
    print("no categ",no_categ)


