from django.db import models
from django.contrib.auth.models import AbstractUser

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#000000')  # Default color is black
    extra_class_taken = models.IntegerField(default=0)  # Tracks the number of extra classes taken
    extra_classes_in_minutes = models.IntegerField(default=0)  # Tracks the total duration of extra classes in minutes
    leave_taken = models.IntegerField(default=0)  # New field for leave taken, default set to zero

    def __str__(self):
        return f"{self.name}"



class Class(models.Model):
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return self.class_name
    
class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name
    

class Period_ID(models.Model):
    period_id = models.CharField(max_length=100)

    def __str__(self):
        return self.period_id
    
class Period(models.Model):
    period_id = models.ForeignKey(Period_ID, on_delete=models.CASCADE, null=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    def __str__(self):
        return f"({self.class_name}, {self.subject}) {self.start_time} - {self.end_time}"


class Room(models.Model):
    room_number = models.IntegerField(unique=True)

    def __str__(self):
        return f"Room {self.room_number}"

class TeacherAvailability(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    available_periods = models.ManyToManyField(Period)

    def __str__(self):
        return f"{self.teacher} - Available Periods"

class AbsenceTracking(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day = models.DateField()

    def __str__(self):
        return f"{self.teacher} - Absent on {self.day}"

class CustomUser(AbstractUser):
    ROLES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    )
    role = models.CharField(max_length=20, choices=ROLES)

class DefaultRoutine(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"Period {self.period.period_id} - {self.assigned_teacher}"
    

class AdjustedSchedule(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField(null=True)

    def __str__(self):
        return f"Period {self.period.period_id} - {self.assigned_teacher}"




