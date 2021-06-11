from django import template
from .models import Course, Student, Enrollee
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import render
from django.contrib import messages

def index(request):
    return HttpResponse("HELLO WORLD!")

def students(request):
    allStudents = Student.objects.order_by('-last_name')[:5]
    context = {'allStudents': allStudents}
    return render(request, 'dashboard/students.html', context)

def courses(request):
    allCourses = Course.objects.order_by('-prefix','number')[:5]
    for c in allCourses:
        try:
            c.enrollee_count = len(Enrollee.objects.filter(course_id=c))
        except:
            c.enrollee_count = 0
    context = {'allCourses': allCourses}
    return render(request, 'dashboard/courses.html', context)

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
    context = {'enrolledCourses': enrolledCourses, 'allStudents': allStudents, 'allCourses': allCourses, 'selectedStudent': targetStudent}
    return render(request, 'dashboard/enrollment.html', context)

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
