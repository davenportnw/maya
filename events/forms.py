# forms.py
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput

class EventForm(forms.Form):    
    date = forms.DateTimeField(
    input_formats=['%d/%m/%Y %H:%M'],
    widget=forms.DateTimeInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-target': '#datetimepicker1'
    })
    )
