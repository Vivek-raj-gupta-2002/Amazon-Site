from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models

class sign_up_form(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput({
        'class': 'auto-group-xszu-Nez', 'placeholder': 'Username'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput({
        'class': 'auto-group-xszu-Nez'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput({
        'class': 'auto-group-xszu-Nez'
    }))

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]


class form_login(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput({
        'class': 'auto-group-xszu-Nez', 'placeholder': 'Username'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput({
        'class': 'auto-group-xszu-Nez'
    }))

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]


class AddCategoryForm(forms.ModelForm):
    name = forms.CharField(label='Catogery Name', widget=forms.TextInput({
        'class': 'auto-group-jhbc-8h4', 'placeholder': 'Category Name'
    }))
    
    class Meta:
        model = models.Catogery
        fields = ['name']

class AddLinkForm(forms.ModelForm):
    product_link = forms.URLField(label='Product Link', widget=forms.URLInput({
        'class': 'auto-group-jhbc-8h4', 'placeholder': 'Product URL'
    }))

    class Meta:
        model = models.Link
        fields = ['product_link']



