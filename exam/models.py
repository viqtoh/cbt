from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.


class Course(models.Model):
	name = models.CharField(max_length=50)
	sections = models.ManyToManyField('Section')
	time = models.IntegerField()
	description = models.CharField(max_length=255, null=True, blank=True)
	submit = models.CharField(max_length=512, null=True,blank=True)
	active = models.BooleanField(default=False)
	last_active = models.DateTimeField(null=True, blank=True)
	show = models.BooleanField(default=False)

class Section(models.Model):
	name = models.CharField(max_length=255)
	questions = models.ManyToManyField('Question', blank=True)

	def __str__(self):
		return (self.name)

class Question(models.Model):
	question = RichTextField(verbose_name='Question')
	options = models.ManyToManyField('Answer')
	image = models.ImageField(upload_to='exams/images/', blank=True, default='')
	answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True, related_name='exam.Question.answer+')

	def __str__(self):
		return (self.question)

class Answer(models.Model):
	answer = models.CharField(max_length=2550)

	def __str__(self):
		return (self.answer)


class StudentDetails(models.Model):
	name = models.CharField(max_length=50)
	passcode = models.CharField(max_length=8)
	exams = models.ManyToManyField('Examination', blank=True)
	reg = models.CharField(max_length=255, blank=True)
	status = models.CharField(max_length=10, default='active')

class Examination(models.Model):
	course = models.ForeignKey('Course',on_delete=models.CASCADE, null=True)
	questions = models.ManyToManyField('Question', blank=True)
	answers = models.ManyToManyField('Answer', blank=True)
	start = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=9, default='running')

	def getscore(self):
		score = 0
		for ans in self.answers.all():
			for quest in self.questions.all():
				if(ans == quest.answer):
					score+=1
		return (score)
	def questionsNo(self):
		sections = self.course.sections.all()
		count = 0
		for section in sections:
			count += section.questions.count()
		return (count)