from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Node(models.Model):
  url_name = models.CharField(max_length=50)  #Would be used for URL
  title = models.CharField(max_length=50) #Would be used for Display Title
  parent = models.ForeignKey('self',null=True,blank=True,related_name='Parent')
  priority = models.IntegerField(default=0)
  visibility = models.BooleanField(default=True)
  external_url = models.CharField(max_length=100,null=True,blank=True)
  level = models.IntegerField(default=0)
  content = RichTextField(default='')
  def __str__(self):
    return self.title + " @ " + str(self.level)
  class Meta:
    app_label = 'website'

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
  class Meta:
    app_label = 'website'


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
  class Meta:
    app_label = 'website'

class Link(models.Model):
  title = models.CharField(max_length=50)
  url = models.CharField(max_length=100)
  visibility = models.BooleanField(default=True)
  priority = models.IntegerField(default=0)
  def __str__(self):
    return self.title
  class Meta:
    app_label = 'website'


class File(models.Model):
  title = models.CharField(max_length=50,unique=True)
  file_added = models.FileField(blank=False,upload_to='website/media/')
  def __str__(self):
    return self.title
  class Meta:
    app_label = 'website'


class PhotoSlider(models.Model):
  title = models.CharField(max_length=50)
  image = models.FileField(blank=False,upload_to='website/media/slider/')
  visibility = models.BooleanField(default=True)
  priority = models.IntegerField(default=0)
  def __str__(self):
    return self.title
  class Meta:
    app_label = 'website'


class DistinguishedAlumni(models.Model):
  CATEGORY_CHOICES = (
        ('Academic Research', 'Academic Research',),
        ('Corporate Development/Adminstration/Entrepreneurship', 'Corporate Development/Adminstration/Entrepreneurship',),
        ('Social Sciences/Engineering and Services/Public Adminstration', 'Social Sciences/Engineering and Services/Public Adminstration',),
        ('Service to Society', 'Service to Society',),
    )
  name = models.CharField(max_length=100)
  dob = models.DateField()
  diploma = models.CharField(max_length=50)
  year = models.IntegerField()
  qualifications = models.TextField(null=True,blank=True)
  address = models.TextField()
  category = models.CharField(max_length=50,choices = CATEGORY_CHOICES)
  description = models.TextField()
  contribution = models.TextField()
  photo = models.ImageField(blank=False,upload_to='website/media/distinguisted/images/')
  resume = models.FileField(blank=False,upload_to='website/media/distinguisted/resumes/')
  optional1 = models.FileField(blank=True,upload_to='website/media/distinguisted/optional/')
  optional2 = models.FileField(blank=True,upload_to='website/media/distinguisted/optional/')
  optional3 = models.FileField(blank=True,upload_to='website/media/distinguisted/optional/')

  def __str__(self):
    return self.name
  class Meta:
    app_label = 'website'

class DistinguishedAlumniNominee(models.Model):
  CATEGORY_CHOICES = (
        ('Academic Research', 'Academic Research',),
        ('Corporate Development/Adminstration/Entrepreneurship', 'Corporate Development/Adminstration/Entrepreneurship',),
        ('Social Sciences/Engineering and Services/Public Adminstration', 'Social Sciences/Engineering and Services/Public Adminstration',),
        ('Service to Society', 'Service to Society',),
    )
  nominee_name = models.CharField(max_length=100)
  nominee_email = models.EmailField()
  nominee_contact = models.CharField(max_length=20)
  nominee_degree = models.CharField(max_length=50)
  nominee_yearpass = models.IntegerField()
  nominee_quals = models.TextField(null=True,blank=True)
  nominee_address = models.TextField()
  nominee_designation = models.CharField(max_length=50)
  nominee_category = models.CharField(max_length=100,choices=CATEGORY_CHOICES)
  nominee_description = models.TextField()
  nominee_webpage = models.CharField(max_length=50,null=True,blank=True)
  nominee_linkedin = models.CharField(max_length=50,null=True,blank=True)
  nominee_awards = models.TextField(null=True,blank=True) 
  nominee_photo = models.ImageField(blank=False,upload_to='website/media/distinguisted/images/')
  nominee_resume = models.FileField(blank=False,upload_to='website/media/distinguisted/resumes/')
  nominee_optional1 = models.FileField(blank=True,upload_to='website/media/distinguisted/optional/')
  def __str__(self):
    return self.nominee_name
  class Meta:
    app_label = 'website'

class DistinguishedAlumniNominator(models.Model):
  CHOICES = (
	('Y','Yes'),
	('N','No'),
	)
  nominee = models.ForeignKey(DistinguishedAlumniNominee)
  nominator_name = models.CharField(max_length=50)
  nominator_email = models.EmailField()
  nominator_contact = models.CharField(max_length=20)
  nominator_designation = models.CharField(max_length=50)
  nominator_address = models.TextField()
  nominator_affiliation = models.TextField()
  nominator_moreinfo = models.CharField(max_length=10,choices=CHOICES)
  def __str__(self):
    return self.nominator_name+" nominated "+self.nominee.nominee_name
  class Meta:
    app_label = 'website'
