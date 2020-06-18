from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Mentors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='Profile')
    name = models.CharField(default='1',max_length=100)
    full_names = models.CharField(default='user',max_length=100)
    emails = models.EmailField(default='user@gmail.com')
    image = CloudinaryField('avatar')
    pdfs = models.FileField(default='user.pdf',upload_to="props/pdfs")
    resume = CloudinaryField('resume')
    prop_no = models.CharField(max_length=10,default='-1',null=True)
    propsl_list = models.CharField(default="0",max_length=300)
    skills = models.CharField(default="[]",max_length=300)
    skill_level = models.CharField(default="{}", max_length=300)
    extracted_skills = models.CharField(default="[]",max_length=300)
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()


class Proposal(models.Model):
    category = models.CharField(default='no text',max_length=500,blank=True)
    ids = models.TextField(default='no id',max_length=10)
    summary = models.TextField(default='no summary',max_length=4000)
    svm_categories = models.CharField(default='no svm categories',max_length=200,blank = True)
    text = models.TextField(default='no text',max_length=10000)
    title =models.CharField(default='no title',max_length=500)
    mentor_assigned=models.CharField(default='no mentor assigned',max_length=100)

    def __str__(self):
        return f'{self.ids}'

