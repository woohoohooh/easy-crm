from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assign', 'estimate_start', 'estimate_finish', 'estimate_team']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }