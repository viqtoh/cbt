from django.db import models

# Create your models here.


class Course(models.Model):
	name = models.CharField(max_length=255)
	sections = models.ManyToManyField('Section')
	time = models.IntegerField()
	recent = models.BooleanField(default=False)

class Section(models.Model):
	name = models.CharField(max_length=255)
	questions = models.ManyToManyField('Question', blank=True, null=True)

	def __str__(self):
		return (self.name)

class Question(models.Model):
	question = models.CharField(max_length=2550)
	options = models.ManyToManyField('Answer')
	answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='exam.Question.answer+')

	def __str__(self):
		return (self.question)

class Answer(models.Model):
	answer = models.CharField(max_length=2550)

	def __str__(self):
		return (self.answer)