from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordResetForm

from ckeditor.widgets import CKEditorWidget

from exam.models import Question


class QuestionForm(forms.ModelForm):
	question = forms.CharField(widget=CKEditorWidget(config_name='default'))

	class Meta:
		model = Question
		fields = ("question", )
