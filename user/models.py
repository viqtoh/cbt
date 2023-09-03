from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
	username = None

	email = models.EmailField(max_length=254, unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = CustomUserManager()

	Gender = models.CharField(max_length=6, null=True, blank=True)
	Phone_number = models.CharField(max_length=20, null=True, blank=True)
	FullName = models.CharField(max_length=2555, null=True, blank=True)
	Feeds = models.ManyToManyField('Feed',blank=True)


	def changeUser(self):
		return reverse('Library:userChange', args=[self.email])

	def editUser(self):
		return reverse('Library:userEdit', args=[self.email])

	def makeLibrarian(self):
		return reverse('Library:makeLibrarian', args=[self.email])
	def getName(self):
		return(self.first_name +" "+ self.last_name)
	def save(self, *args, **kwargs):
		if self.FullName == None:
			self.FullName = self.getName()
		super().save(*args,**kwargs)

	def __str__(self):
		return(self.first_name +" "+ self.last_name)
			
	def justName(self):
		return(self.first_name +" "+ self.last_name)

class Feed(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)

