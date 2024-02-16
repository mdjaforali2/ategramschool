from django.contrib import admin
from .models import Teacher, Class, Period_ID, Period, Subject, Room, TeacherAvailability, AbsenceTracking, CustomUser, DefaultRoutine, AdjustedSchedule

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'leave_taken', 'extra_class_taken', 'extra_classes_in_minutes', ]

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_name']

@admin.register(Period_ID)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['period_id']

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['period_id', 'class_name', 'subject']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number']

@admin.register(TeacherAvailability)
class TeacherAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'get_available_periods']

    def get_available_periods(self, obj):
        return ", ".join([str(period) for period in obj.available_periods.all()])

@admin.register(AbsenceTracking)
class AbsentTeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'day']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']

@admin.register(DefaultRoutine)
class DefaultRoutineAdmin(admin.ModelAdmin):
    list_display = ['period', 'assigned_teacher']


@admin.register(AdjustedSchedule)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['period', 'assigned_teacher', 'date']
