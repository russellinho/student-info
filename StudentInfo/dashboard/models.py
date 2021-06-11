from django.db import models

class Student(models.Model):
    def __str__(self):
        return self.last_name + ', ' + self.first_name
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    major = models.CharField(max_length=20, default='')
    year = models.CharField(max_length=20, default='Freshman')
    gpa = models.DecimalField(default=4.0, decimal_places=2, max_digits=3)
    enroll_date = models.DateTimeField('date published')

class Course(models.Model):
    def __str__(self):
        return self.prefix + str(self.number)
    number = models.IntegerField()
    prefix = models.CharField(max_length=3)
    max_students = models.IntegerField(default=20)

class Enrollee(models.Model):
    def __str__(self):
        return str(self.student_id) + ', ' + str(self.course_id)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
