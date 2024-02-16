from django.urls import path
from . import views
from .views import RegularScheduleView, handle_teacher_absence_logic, request_absent_form, RegularScheduleView, adjusted_schedule, TemporarySchedulesView


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('academics/', views.academics, name='academics'),
    path('admissions/', views.admissions, name='admissions'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'),  # Add login URL
    path('signup/', views.user_signup, name='signup'),  # Add signup URL
    path('logout/', views.user_logout, name='logout'),  # Add logout URL
    path('regular-schedule/', RegularScheduleView.as_view(), name='regular_schedule'),
    path('handle-absence/', handle_teacher_absence_logic, name='handle_absence'),
    path('request-absent-form/', request_absent_form, name='request_absent_form'),
    path('temporary-schedules/', TemporarySchedulesView.as_view(), name='temporary_schedules'),
    path('adjusted-schedule/<str:date>/', views.adjusted_schedule, name='adjusted_schedule'),



]
