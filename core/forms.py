# forms.py
from django import forms
from .models import Teacher
from django.utils.translation import gettext_lazy as _

class TeacherAbsenceForm(forms.Form):
    absent_teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        label=_('Absent Teacher'),
        required=True,
        empty_label=None
    )
    absence_date = forms.DateField(
        label=_('Absence Date'),
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
