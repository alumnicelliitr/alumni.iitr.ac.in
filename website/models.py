from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Node(models.Model):
  title = models.CharField(max_length=20)
  parent = models.ForeignKey('self',null=True,blank=True,related_name='Parent')
  priority = models.IntegerField(default=0)
  visibility = models.BooleanField(default=True)
  url = models.CharField(max_length=100,null=True,blank=True)
  level = models.IntegerField(default=0)
  content = RichTextField(default='')
  def __str__(self):
    return self.title

class News(models.Model):
  title = models.CharField(max_length=50)
  short_description = models.CharField(max_length=200)
  url = models.CharField(max_length=100,null=True,blank=True)
  publish = models.DateField()
  expiry = models.DateField()
  priority = models.IntegerField(default=0)
  visibility = models.BooleanField(default=True)
  def __str__(self):
    return self.title

class Event(models.Model):
  title = models.CharField(max_length=50)
  short_description = models.CharField(max_length=200)
  url = models.CharField(max_length=100,null=True,blank=True)
  event_date = models.DateField()
  expiry_date = models.DateField()
  priority = models.IntegerField(default=0)
  visibility = models.BooleanField(default=True)
  def __str__(self):
    return self.title

class Link(models.Model):
  title = models.CharField(max_length=50)
  url = models.CharField(max_length=100)
  visibility = models.BooleanField(default=True)
  priority = models.IntegerField(default=0)
  def __str__(self):
    return self.title
