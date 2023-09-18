from django import template
from ..models import *
import math

register = template.Library()

@register.simple_tag
def checklet(num):
	lets =('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
	return (lets[num-1].upper())

@register.simple_tag
def getlength():
	courseL = Course.objects.all().count()
	#length = courseL /3
	length = 5 / 3
	length = math.ceil(length)
	return (length)

@register.simple_tag
def checkans(passcode, question_id):
	student = StudentDetails.objects.filter(passcode=passcode).first()
	exam = student.exams.filter(course__active=True).first()
	question = exam.questions.filter(id=question_id).first()
	if(question == None):
		return False
	else:
		return True

@register.filter
def page_window(page, last, size=7):
    if page < size // 2 + 1:
        return range(1, min(size+1, last + 1)) # remember the range function won't 
                                                # include the upper bound in the output
    else:
        return range(page - size // 2, min(last + 1, page + 1 + size // 2))


@register.simple_tag
def getexam(student_id, course_id):
	course = Course.objects.filter(id=course_id).first()
	student = StudentDetails.objects.filter(id=student_id).first()
	exam = student.exams.filter(course=course).first()
	return (exam)

@register.simple_tag
def checkans2(exam_id, ans_id):
	exam = Examination.objects.filter(id=exam_id).first()
	ans = Answer.objects.filter(id=ans_id).first()
	got = exam.answers.filter(id=ans_id).first()
	if(got == None):
		return False
	else:
		return True

@register.simple_tag
def checkcorrect(question_id, ans_id):
	question = Question.objects.filter(id=question_id).first()
	ans = Answer.objects.filter(id=ans_id).first()
	if(question.answer == ans):
		return True
	else:
		return False

