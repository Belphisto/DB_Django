from dataclasses import fields
from turtle import update
from django import forms
from django.forms import HiddenInput

MANGA_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

from store.models import Manga, Order

class MangaForm(forms.Form):
    name = forms.CharField(max_length=30, label="Manga", initial="BaseName", required=True)
    author = forms.CharField(max_length=30, label="Author", initial="BaseAuthorName", required=True)
    price = forms.FloatField(min_value = 0, initial=0.0, help_text="enter a non-negative number", required=True)

class editForm(forms.Form):
    name = forms.CharField(max_length=30, label="Manga",  required=True)
    author = forms.CharField(max_length=30, label="Author" ,  required=True)
    price = forms.FloatField(min_value = 0 , help_text="enter a non-negative number", required=True)

class RegForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    login = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'login'}))
    password = forms.CharField(max_length=16, min_length=8, widget=forms.PasswordInput(attrs={'class': 'password'}), required=True, help_text="enter from 8 to 16 characters")
    mail = forms.CharField(max_length=254, required=True,
        widget=forms.TextInput(attrs={'class': 'mail'}))

class LoginForm(forms.Form):
    login = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=16, min_length=8, widget=forms.PasswordInput, required=True, help_text="enter from 8 to 16 characters")

class EditUserForm(forms.Form):
    login =forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    role = forms.IntegerField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    name = forms.CharField(max_length=30)
    mail = forms.EmailField(max_length=254)
    last_password = forms.CharField(max_length=16, min_length=8, widget=forms.PasswordInput, required=False, help_text="enter from 8 to 16 characters")
    new_password = forms.CharField(max_length=16, min_length=8, widget=forms.PasswordInput, required=False, help_text="enter from 8 to 16 characters")

class MangaAddCartForm(forms.Form):
    name = forms.CharField(max_length=30, label="Manga",  required=False, widget = forms.TextInput(attrs={'readonly':'readonly'}))
    author = forms.CharField(max_length=30, label="Author" ,  required=False, widget = forms.TextInput(attrs={'readonly':'readonly'}))
    price = forms.FloatField(min_value = 0 , required=False, widget = forms.TextInput(attrs={'readonly':'readonly'}))
    quantity = forms.TypedChoiceField(choices=MANGA_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=HiddenInput)

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['login', 'name']