# forms.py
from django import forms
from .models import AddBook

class BookForm(forms.Form):
    book_id=forms.CharField(
        label='Book ID',
        widget=forms.TextInput(attrs={'class': 'form-control','style': 'margin-bottom: 10px;'})
        )
    title  =forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control','style': 'margin-bottom: 10px;'})
        )
