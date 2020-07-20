from django import forms

from .models import ErrorReport, SignUp


class ErrorReportForm(forms.ModelForm):
    class Meta:
        model = ErrorReport
        fields = ['email', 'message', ]


class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['full_name', 'email']
