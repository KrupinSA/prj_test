from django.forms import ModelForm
from .models import TaskCalendar


class TaskCalendarForm(ModelForm):
    class Meta:
        model = TaskCalendar
        fields = ('title', 'description', 'date')
    
