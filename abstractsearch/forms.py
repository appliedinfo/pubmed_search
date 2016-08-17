# -- encoding: utf-8 --

# Django
from django import forms
# from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
from django.forms import extras
from django.conf import settings


class SearchForm(forms.Form):

    query = forms.CharField(widget=forms.TextInput(
        attrs={
               'class': 'form-control',
               'id': 'terms',
               'placeholder':"e.g septra"
               }))
    
    # password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={
    #            'class': 'form-control',
    #            'id': 'password',
    #            'required': 'required',
    #            }))