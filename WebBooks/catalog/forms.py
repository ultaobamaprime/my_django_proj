from django import forms
from datetime import date
from django.forms import ModelForm

from .models import Book

class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title','genre','language','author','summary','isbn',]





class Authorsform(forms.Form):
    firstname = forms.CharField(label='name of author')
    lastname = forms.CharField(label='lastname of author')
    date_of_birth = forms.DateField(label='date of birth', initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type':'date'}))
    date_of_death = forms.DateField(label='date of death', initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))