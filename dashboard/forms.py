from django import forms
from django.forms import ModelForm

from .models import Nursery, Task, Workers


class AddTaskForm(ModelForm):
    deadline = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"], required=False)

    class Meta:
        model = Task
        exclude = ['user']


class NurseryForm(ModelForm):
    class Meta:
        model = Nursery
        fields = '__all__'


class AddWorker(ModelForm):
    class Meta:
        model = Workers
        fields = '__all__'
