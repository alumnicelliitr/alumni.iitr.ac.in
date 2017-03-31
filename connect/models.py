from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group
import model_constants as MC
from datetime import datetime

# Create your models here.
class User(AbstractUser,models.Model):
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
		db_table = 'nucleus_user'
		app_label = 'channeli'

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
		verbose_name_plural = 'Branches'
		db_table = 'nucleus_branch'
		app_label = 'channeli'

	def __unicode__(self):
		return self.code + ':' + self.name + '(' + self.graduation + ')'

class Student(models.Model):
	datetime_created = models.DateTimeField(auto_now_add=True)
	semester = models.CharField(max_length=10,blank=True,null=True)
	semester_no = models.IntegerField()
	admission_year = models.IntegerField(verbose_name='Admission Year')
	admission_semtype = models.CharField(max_length=1,choices=MC.SEMESTER_TYPE_CHOICES,verbose_name='Admission Semester')
	cgpa = models.CharField(max_length=6, blank=True)
	bhawan = models.CharField(max_length=MC.CODE_LENGTH,choices=MC.BHAWAN_CHOICES, null=True, blank=True, default=None)
	room_no = models.CharField(max_length=MC.CODE_LENGTH, blank=True,verbose_name='Room No')
	passout_year = models.IntegerField(null=True, blank=True)
	user = models.OneToOneField(User, primary_key=True, parent_link=True)
	branch = models.ForeignKey(Branch)

	class Meta:
		db_table = 'nucleus_student'
		app_label = 'channeli'

class Alumni(models.Model):
	datetime_created = models.DateTimeField(auto_now_add=True)
	student = models.ForeignKey(Student)
	linked_in = models.CharField(max_length=MC.TEXT_LENGTH)
	website = models.CharField(max_length=MC.TEXT_LENGTH)

	class Meta:
		db_table = 'nucleus_alumni'
		app_label = 'channeli'