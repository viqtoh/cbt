from django.urls import path, include

from . import views

app_name = 'user'

urlpatterns = [
    path('signin/', views.sign_in, name="sign_in"),
    path('register/complete0020registrations0020email0020address00202D0020/<str:email>/and0020first0020name00202D0020<str:first_name>/and0020last0020name00202D2D0020<str:last_name>/', views.sign_up_complete, name="sign_up_complete"),
    path('register/successful/', views.sign_up_success, name="sign_up_success"),
    path('signout/', views.sign_out, name="sign_out"),
    path('', views.home, name='home'),
    path('admin/', views.admin, name='admin'),
    path('admin/section/<str:id>/', views.sections, name='sections'),
    path('admin/section/questions/<str:id>/', views.questions, name='questions'),
    path('admin/section/questions/<str:id>/<str:question_id>/edit/', views.editquestion, name='editquestion'),
    path('admin/section/questions/<str:section_id>/delete/<str:id>/', views.deleteQ, name='deleteQ'),
    path('admin/delete/exam/<str:id>/', views.deleteCourse, name='deleteCourse'),
    path('admin/delete/exam/section/<str:id>/', views.deleteSection, name='deleteSection'),
    path('admin/exam/add/section/<str:id>/', views.addSection, name='addSection'),
    path('admin/exam/make/active/<str:id>/', views.makeActive, name='makeActive'),
    path('admin/students/', views.studentDetails, name='students'),
    path('admin/students/search/<str:search>/', views.studentDetailsSearch, name='studentsSearch'),
    path('admin/examinations/', views.examinations, name='exams'),
    path('admin/examinations/course/<str:id>/search/<str:search>/', views.examinationSearch, name='examSearch'),
    path('admin/examinations/course/<str:id>', views.examination, name='exam'),
    path('admin/examinations/course/<str:course_id>/paper/<str:id>/', views.paper, name='paper'),
    path('admin/examinations/course/<str:course_id>/examination/<str:id>/delete/', views.deleteexam, name='deleteexam'),
    ]
    