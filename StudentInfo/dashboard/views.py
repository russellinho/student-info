from functools import total_ordering
from django import template
from .models import Course, Student, Enrollee
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    context = {'username': request.POST.get('username', '')}
    return render(request, 'auth.html', context)

def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/dashboard/login')

def auth(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    myUsername = request.POST.get('usernameInput', '')
    myPassword = request.POST.get('passwordInput', '')
    userAuthenticated = authenticate(request, username=myUsername, password=myPassword)
    if userAuthenticated is None:
        # Auth failed
        messages.error(request, "Invalid username and/or password!")
        return HttpResponseRedirect('/dashboard/login')
    
    django_login(request, userAuthenticated)
    print(request.GET.get("next", '/dashboard'))
    return HttpResponseRedirect(request.GET.get("next", '/dashboard'))

@login_required
def index(request):
    name = request.user.first_name
    allStudents = Student.objects.all()
    allCourses = Course.objects.all()
    for course in allCourses:
        course.enrollees = len(Enrollee.objects.filter(course_id=course))
    allCourses = sorted(allCourses, key=lambda course: course.enrollees, reverse=True)
    freshmenCount = len(Student.objects.filter(year='Freshman'))
    sophomoreCount = len(Student.objects.filter(year='Sophomore'))
    juniorCount = len(Student.objects.filter(year='Junior'))
    seniorCount = len(Student.objects.filter(year='Senior'))
    totalGpa = 0.0
    totalStudents = 0
    for student in allStudents:
        totalGpa += float(student.gpa)
        totalStudents += 1
    if totalStudents == 0:
        totalStudents = 1
    context = {'myUsername': name, 'freshmen': freshmenCount, 'sophomores': sophomoreCount, 'juniors': juniorCount, 'seniors': seniorCount, 'students': totalStudents, 'gpa': totalGpa / totalStudents,
            'courses': len(allCourses), 'course1': allCourses[0], 'course2': allCourses[1], 'course3': allCourses[2], 'page': 0}
    return render(request, 'dashboard/home.html', context)

@login_required
def students(request):
    allStudents = Student.objects.order_by('-last_name')[:5]
    context = {'allStudents': allStudents, 'page': 1}
    return render(request, 'dashboard/students.html', context)

@login_required
def courses(request):
    allCourses = Course.objects.order_by('-prefix','number')[:5]
    for c in allCourses:
        try:
            c.enrollee_count = len(Enrollee.objects.filter(course_id=c))
        except:
            c.enrollee_count = 0
    context = {'allCourses': allCourses, 'page': 2}
    return render(request, 'dashboard/courses.html', context)

@login_required
def enrollment(request):
    studentId = request.GET.get('student', -1)
    allStudents = Student.objects.order_by('-last_name')[:5]
    allCourses = Course.objects.all()
    enrolledCourses = None
    targetStudent = None
    try:
        targetStudent = Student.objects.get(id=studentId)
        enrolledCourses = []
        for e in Enrollee.objects.filter(student_id=targetStudent):
            enrolledCourses.append({"prefix": e.course_id.prefix, "number": e.course_id.number})
    except Exception as ex:
        enrolledCourses = None
    context = {'enrolledCourses': enrolledCourses, 'allStudents': allStudents, 'allCourses': allCourses, 'selectedStudent': targetStudent, 'page': 3}
    return render(request, 'dashboard/enrollment.html', context)

@login_required
def enrollStudentInCourse(request):
    studentId = request.POST.get('student', -1)
    courseId = request.POST.get('course', -1)
    # check if course is already full
    targetCourse = Course.objects.get(id=courseId)
    targetStudent = Student.objects.get(id=studentId)
    currStudentCount = len(Enrollee.objects.filter(course_id=targetCourse))
    if currStudentCount >= targetCourse.max_students:
        messages.error(request, "This course has already reached the maximum number of students!")
        # redirect back to enrollment page with same details
        return HttpResponseRedirect('enrollment/?student=' + str(studentId))
    # ensure that the student is not already enrolled in 3 courses
    if len(Enrollee.objects.filter(student_id=targetStudent)) >= 3:
        messages.error(request, "You're already enrolled in three or more courses!")
        return HttpResponseRedirect('enrollment/?student=' + str(studentId))
    # ensure that the student is not already enrolled in the course
    if len(Enrollee.objects.filter(student_id=targetStudent, course_id=targetCourse)) == 1:
        messages.error(request, "You're already enrolled in this course!")
        return HttpResponseRedirect('enrollment/?student=' + str(studentId))
    # add and save the student to the course
    Enrollee(student_id=targetStudent, course_id=targetCourse).save()
    messages.success(request, "Enrollment successful!")
    # redirect back to enrollment page with same details
    return HttpResponseRedirect('enrollment/?student=' + str(studentId))
