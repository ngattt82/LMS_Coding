from django import forms
from django.contrib.auth.forms import AuthenticationForm


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label="Upload Excel File")



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
