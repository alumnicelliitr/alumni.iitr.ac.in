from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Tabs(models.Model):
  title = models.CharField(max_length=20)
  priority = models.IntegerField(default=0)
  visibility = models.BooleanField(initial=True)
  def __str__(self):
    return self.title + "@" + self.priority

class Page(models.Model):
  title = models.CharField(max_length=200)
  parent = models.ForeignKey(Tabs)
  visibility = models.BooleanField(initial=True)
  content = RichTextField()
  def __str__(self):
    return self.title + "-" + self.parent.title
