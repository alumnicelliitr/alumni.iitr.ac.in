from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from encrypted_id.models import EncryptedIDModel
import model_constants as MC
from datetime import datetime
from taggit.managers import TaggableManager

# Create your models here.
class User(AbstractUser,  models.Model):
  datetime_created = models.DateTimeField(auto_now_add=True)
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  photo = models.CharField(max_length=100,null=True, blank=True)
  gender = models.CharField(max_length=1)
  birth_date = models.DateField(blank=True, null=True,verbose_name='Date of Birth')
  contact_no = models.CharField(max_length=20, null=True, blank=True,verbose_name='Contact No')
  def save(self, *args, **kwargs):
    if not self.datetime_created:
      self.datetime_created = datetime.now()
    super(User,self).save(*args,**kwargs)
  class Meta:
    managed = False
    db_table = 'nucleus_user'
    app_label = 'connect'

class Branch(models.Model):
  code = models.CharField(max_length=MC.CODE_LENGTH, primary_key=True)
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  degree = models.CharField(max_length=MC.CODE_LENGTH,choices=MC.DEGREE_CHOICES)
  department = models.CharField(max_length=MC.CODE_LENGTH,choices=MC.DEPARTMENT_CHOICES)
  graduation = models.CharField(max_length=MC.CODE_LENGTH,choices=MC.GRADUATION_CHOICES)
  no_of_semesters = models.IntegerField(null=True, blank=True)

  @property
  def duration(self):
    return self.no_of_semesters

  class Meta:
    managed = False
    verbose_name_plural = 'Branches'
    db_table = 'nucleus_branch'
    app_label = 'connect'

  def __unicode__(self):
    return self.code + ':' + self.name + '(' + self.graduation + ')'

class Student(models.Model):
  user = models.OneToOneField(User, primary_key=True, parent_link=True)
  datetime_created = models.DateTimeField(auto_now_add=True)
  semester = models.CharField(max_length=10,blank=True,null=True)
  semester_no = models.IntegerField()
  admission_year = models.IntegerField(verbose_name='Admission Year')
  admission_semtype = models.CharField(max_length=1,choices=MC.SEMESTER_TYPE_CHOICES,verbose_name='Admission Semester')
  cgpa = models.CharField(max_length=6, blank=True)
  bhawan = models.CharField(max_length=MC.CODE_LENGTH,choices=MC.BHAWAN_CHOICES, null=True, blank=True, default=None)
  room_no = models.CharField(max_length=MC.CODE_LENGTH, blank=True,verbose_name='Room No')
  passout_year = models.IntegerField(null=True, blank=True)
  branch = models.ForeignKey(Branch)

  class Meta:
    managed = False
    db_table = 'nucleus_student'
    app_label = 'connect'

class Alumni(models.Model):
  user = models.OneToOneField(User)
  datetime_created = models.DateTimeField(auto_now_add=True)
  admission_year = models.IntegerField(verbose_name='Admission Year')
  passout_year = models.IntegerField(null=True, blank=True)
  branch = models.ForeignKey(Branch)
  linked_in = models.CharField(max_length=MC.TEXT_LENGTH,blank=True)
  facebook = models.CharField(max_length=MC.TEXT_LENGTH,blank=True)
  website = models.CharField(max_length=MC.TEXT_LENGTH,blank=True)
  profile = models.CharField(max_length=MC.TEXT_LENGTH,blank=True)
  company = models.CharField(max_length=MC.TEXT_LENGTH,blank=True)
  email = models.EmailField(max_length=150)
  tags = TaggableManager()

  def __str__(self):
    return self.user.username
  class Meta:
    db_table = 'nucleus_arc_alumni'
    app_label = 'connect'

class Chat(models.Model):
  sender = models.ForeignKey(User, related_name='message_sender')
  receiver = models.ForeignKey(User, related_name='message_receiver')
  message = models.CharField(max_length=1000)
  datetime_created = models.DateTimeField(auto_now_add=True)
  is_read = models.BooleanField(default=False)

  def __str__(self):
    return self.sender.username + " to " + self.receiver.username
  class Meta:
    db_table = 'nucleus_arc_chat'
    app_label = 'connect'

class ChatRequest(EncryptedIDModel):
  sender = models.ForeignKey(User, related_name='request_sender')
  receiver = models.ForeignKey(User, related_name='request_receiver')
  datetime_created = models.DateTimeField(auto_now_add=True)


  class Meta:
    db_table = 'nucleus_arc_chat_request'
    app_label = 'connect'
