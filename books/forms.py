# forms.py
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Cari Buku', max_length=200)
