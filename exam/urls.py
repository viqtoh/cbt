from django.urls import path, include

from . import views

app_name = 'exam'

urlpatterns = [
    path('exam/<str:passcode>/page/course/<int:active>/<int:question>', views.examPage, name="exampage"),
    path('welcome/test/pass/entry/welcome/<str:passcode>/', views.welcome, name="welcome"),
    path('submitted/logout/<str:passcode>/', views.submitted, name='submitted')
    ]
    