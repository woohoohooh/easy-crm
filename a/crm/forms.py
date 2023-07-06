from django import forms
from .models import Task, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class TaskForm(forms.ModelForm):
    comment_form = CommentForm()
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assign', 'estimate_start', 'estimate_finish', 'estimate_team']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }