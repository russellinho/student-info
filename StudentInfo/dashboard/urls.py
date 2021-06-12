from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('auth/', views.auth, name='auth'),
    path('students/', views.students, name='students'),
    path('courses/', views.courses, name='courses'),
    path('enrollment/<int:student_id>', views.enrollment, name='enrollment'),
    path('enrollment/', views.enrollment, name='enrollment'),
    path('enrollStudentInCourse', views.enrollStudentInCourse, name='enrollStudentInCourse'),
]