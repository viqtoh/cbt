from django.urls import path, include

from . import views

app_name = 'user'

urlpatterns = [
    path('signin/', views.sign_in, name="sign_in"),
    path('register/', views.sign_up, name="sign_up"),
    path('register/complete0020registrations0020email0020address00202D0020/<str:email>/and0020first0020name00202D0020<str:first_name>/and0020last0020name00202D2D0020<str:last_name>/', views.sign_up_complete, name="sign_up_complete"),
    path('register/successful', views.sign_up_success, name="sign_up_success"),
    path('signout/', views.sign_out, name="sign_out"),
    path('', views.home, name='home'),
    ]
    