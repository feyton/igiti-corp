from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import UserCreationForm
from store.models import Address
from .models import User

class CreateUserForm(UserCreationForm):
    """
    New User Form. Requires password confirmation.
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    profile_image = forms.ImageField(allow_empty_file=True, required=False)
    biography = forms.CharField(max_length=255, required=False)
    country = CountryField(blank_label='(select country)').formfield(
        required=False, widget=CountrySelectWidget(attrs={
            'class': 'custom-select my-1 width-90',
            'value': 'RW' }))
            
    class Meta:
        model = Address
        fields = ['city', 'district', 'street_address']
        required = []
