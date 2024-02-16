from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import TeacherAbsenceForm
from .models import Teacher, DefaultRoutine, Period, Class, TeacherAvailability, AbsenceTracking, AdjustedSchedule
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def academics(request):
    return render(request, 'academics.html')

def admissions(request):
    return render(request, 'admissions.html')

def contact(request):
    return render(request, 'contact.html')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = request.POST.get('role')  # Assuming you have a 'role' field in your User model
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

from django.db.models import Q

class RegularScheduleView(TemplateView):
    template_name = 'regular_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve all classes
        classes = Class.objects.all()
        class_schedules = {}

        # Group periods by unique start and end times
        unique_periods = self.get_unique_periods(Period.objects.all())

        for class_instance in classes:
            # Filter all default routines for the class
            default_routines = DefaultRoutine.objects.filter(period__class_name=class_instance)

            class_schedule = {period: None for period in unique_periods}
            
            # Populate class schedule with routines
            for routine in default_routines:
                class_schedule[routine.period] = routine

            class_schedules[class_instance] = class_schedule

        context['class_schedules'] = class_schedules
        context['unique_periods'] = unique_periods
        return context

    def get_unique_periods(self, periods):
        unique_periods = {}
        for period in periods:
            period_key = (period.start_time, period.end_time)
            if period_key not in unique_periods:
                unique_periods[period_key] = period
        return unique_periods.values()




# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import TeacherAbsenceForm
from .models import Teacher, DefaultRoutine, Period, Class, TeacherAvailability, AbsenceTracking, AdjustedSchedule
from django.db.models import Q, Count
import random
from datetime import datetime, timedelta


@login_required
def request_absent_form(request):
    absences = AbsenceTracking.objects.all()

    if request.method == 'POST':
        form = TeacherAbsenceForm(request.POST)
        if form.is_valid():
            absent_teacher = form.cleaned_data['absent_teacher']
            absence_date = form.cleaned_data['absence_date']
                # Update the leave taken for the absent teacher
            absent_teacher.leave_taken += 1
            absent_teacher.save()
            # Handle teacher absence logic
            handle_teacher_absence_logic(absent_teacher, absence_date)
            
            # Create an AbsenceTracking object and save it to the database
            AbsenceTracking.objects.create(teacher=absent_teacher, day=absence_date)
            
            return redirect('request_absent_form')
    else:
        form = TeacherAbsenceForm()
    return render(request, 'request_absent_form.html', {'form': form, 'absences': absences})



# Your function definition and imports...

def handle_teacher_absence_logic(absent_teacher, absence_date):
    max_over_class_per_teacher_per_day = 2  # Define a maximum number of classes per teacher per day

    # Retrieve the absent teacher's classes
    absent_teacher_classes = DefaultRoutine.objects.filter(assigned_teacher=absent_teacher)

    # Create a dictionary to store the count of classes assigned to each teacher
    teacher_class_counts = {}

    # Retrieve available teachers for each period
    for default_routine in absent_teacher_classes:
        period = default_routine.period

        # Retrieve available teachers for the current period
        available_teachers_for_period = TeacherAvailability.objects.filter(available_periods=period)

        if available_teachers_for_period.exists():
            # Initialize the class count for each teacher if not already initialized
            for teacher_availability in available_teachers_for_period:
                teacher = teacher_availability.teacher
                if teacher not in teacher_class_counts:
                    teacher_class_counts[teacher] = 0

            # Determine the minimum count among the teachers
            min_assigned_teacher_count = min(teacher_class_counts.values(), default=0)

            # Check if there are multiple teachers with the same minimum count
            teachers_with_min_count = [teacher for teacher, count in teacher_class_counts.items() if count == min_assigned_teacher_count]
            print(teachers_with_min_count)

            if len(teachers_with_min_count) == 1:
                # If there's only one teacher with the minimum count, sort teachers by workload count
                teacher = teachers_with_min_count[0]  # Get the first teacher with the minimum count
                if teacher_class_counts[teacher] <= max_over_class_per_teacher_per_day:

                    period_start = datetime.combine(datetime.min, period.start_time)
                    period_end = datetime.combine(datetime.min, period.end_time)

                    # Update the teacher's extra class taken count
                    teacher.extra_class_taken += 1

                    # Calculate period duration in minutes
                    period_duration_minutes = (period_end - period_start).seconds // 60
                    teacher.extra_classes_in_minutes += period_duration_minutes

                    # Assign the period to the teacher for the absence date
                    assign_period_to_teacher(period, teacher_availability, absence_date)
                    teacher.save()

                    # Update the class count for the teacher
                    teacher_class_counts[teacher] += 1
                    print(teacher)
                    print(teacher_class_counts)
                    


            else:
                # If there are multiple teachers with the minimum count, sort them by count
                sorted_teachers = sorted(available_teachers_for_period, key=lambda x: teacher_class_counts[x.teacher])

                # Loop through available teachers round-robin style
                for teacher_availability in sorted_teachers:
                    teacher = teacher_availability.teacher

                    print(teacher , "from outblock")
                    # Check if the teacher's workload is within the maximum limit
                    if teacher_class_counts[teacher] <= max_over_class_per_teacher_per_day:
                        # Inside the handle_teacher_absence_logic_round_robin function
                        period_start = datetime.combine(datetime.min, period.start_time)
                        period_end = datetime.combine(datetime.min, period.end_time)

                        # Update the teacher's extra class taken count
                        teacher.extra_class_taken += 1

                        # Calculate period duration in minutes
                        period_duration_minutes = (period_end - period_start).seconds // 60
                        teacher.extra_classes_in_minutes += period_duration_minutes

                        # Assign the period to the teacher for the absence date
                        assign_period_to_teacher(period, teacher_availability, absence_date)
                        teacher.save()

                        # Update the class count for the teacher
                        teacher_class_counts[teacher] += 1
                        print(teacher)
                        print(teacher_class_counts)
                        break  # Break the loop after assigning to one teacher


# Your assign_period_to_teacher function and other parts of the code...




# Your assign_period_to_teacher function and other parts of the code...
def assign_period_to_teacher(period, teacher_availability, absence_date):
    # Access the teacher instance from the teacher availability
    teacher = teacher_availability.teacher

    # Assign the period to the teacher for the absence date
    AdjustedSchedule.objects.create(period=period, assigned_teacher=teacher, date=absence_date)






from django.shortcuts import render
from django.views import View
from .models import AbsenceTracking

class TemporarySchedulesView(View):
    def get(self, request):
        # Retrieve all absences
        absences = AbsenceTracking.objects.all()

        # Pass the absences to the template for rendering
        context = {
            'absences': absences
        }

        # Render the template with the absences data
        return render(request, 'temporary_schedules.html', context)





from datetime import timedelta
def adjusted_schedule(request, date):
    # Retrieve all classes
    classes = Class.objects.all()
    class_schedules = {}

    # Group periods by unique start and end times
    unique_periods = get_unique_periods(Period.objects.all())

    # Filter AdjustedSchedule objects for the given date
    adjusted_schedules = AdjustedSchedule.objects.filter(date=date)

    # Extract period IDs from AdjustedSchedule objects
    adjusted_schedule_period_ids = set(adjusted_schedule.period.period_id for adjusted_schedule in adjusted_schedules)

    # Filter DefaultRoutine objects, excluding those with period IDs present in AdjustedSchedule
    default_routines = DefaultRoutine.objects.exclude(period__period_id__in=adjusted_schedule_period_ids)

    # Initialize teacher statistics dictionary
    teacher_stats = {}

    # Iterate over classes
    for class_instance in classes:
        # Initialize class schedule dictionary
        class_schedule = {period: None for period in unique_periods}

        # Filter all default routines for the class
        routines = default_routines.filter(period__class_name=class_instance).order_by('period__start_time')
        updated_routines = adjusted_schedules.filter(period__class_name=class_instance).order_by('period__start_time')

        # Populate class schedule with routines
        for routine in routines:
            class_schedule[routine.period] = routine

            # Update teacher statistics
            update_teacher_statistics(teacher_stats, routine)

        for routine in updated_routines:
            class_schedule[routine.period] = routine

            # Update teacher statistics
            update_teacher_statistics(teacher_stats, routine)

        # Add class schedule to the dictionary of class schedules
        class_schedules[class_instance] = class_schedule

    context = {
        'class_schedules': class_schedules,
        'unique_periods': unique_periods,
        'date': date,
        'teacher_stats': teacher_stats,
    }

    return render(request, 'adjusted_schedule.html', context)


def update_teacher_statistics(teacher_stats, routine):
    teacher = routine.assigned_teacher
    period_duration = timedelta(hours=routine.period.end_time.hour - routine.period.start_time.hour)

    if teacher not in teacher_stats:
        teacher_stats[teacher] = {
            'num_periods': 1,
            'total_hours': period_duration,
        }
    else:
        teacher_stats[teacher]['num_periods'] += 1
        teacher_stats[teacher]['total_hours'] += period_duration


def get_unique_periods(periods):
    unique_periods = {}
    for period in periods:
        period_key = (period.start_time, period.end_time)
        if period_key not in unique_periods:
            unique_periods[period_key] = period
    return unique_periods.values()











#My own functions to perform certain operation 



from .models import Teacher, Period, TeacherAvailability
from django.db.models import Q

def update_teacher_availability():
    # Get all periods
    periods = Period.objects.all()

    # Iterate through each teacher
    for teacher in Teacher.objects.all():
        # Get all periods where the teacher is assigned
        assigned_periods = Period.objects.filter(defaultroutine__assigned_teacher=teacher)

        # Exclude periods with the same starting time as assigned periods
        available_periods = periods.exclude(
            Q(start_time__in=assigned_periods.values_list('start_time', flat=True))
        )

        # Retrieve or create a TeacherAvailability instance for the current teacher
        teacher_availability, created = TeacherAvailability.objects.get_or_create(teacher=teacher)

        # Set the available periods for the teacher
        teacher_availability.available_periods.set(available_periods)

    print("Teacher availability updated successfully.")



def reset_teacher_values():
    try:
        # Update all instances of the Teacher model to set the specified fields to 0
        Teacher.objects.all().update(extra_class_taken=0, extra_classes_in_minutes=0, leave_taken=0)
        print("Values reset successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")