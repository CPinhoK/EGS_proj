from typing_extensions import NotRequired
from django import forms

class SearchForm(forms.Form):
    querysearch = forms.CharField(label="querysearch", max_length=100)