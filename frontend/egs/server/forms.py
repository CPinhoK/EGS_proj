from typing_extensions import NotRequired
from django import forms

class SearchForm(forms.Form):
    querysearch = forms.CharField(label="querysearch", max_length=100)

class AddProductForm(forms.Form):
    idproduct = forms.IntegerField(label="idproduct")
    nameproduct = forms.CharField(label="nameproduct", max_length=100)
    priceproduct = forms.FloatField(label="priceproduct")
    imageproduct = forms.ImageField(label="imageproduct", required=False)
    categoryproduct = forms.IntegerField(label="categoryproduct")
    statusproduct = forms.CharField(label="statusproduct",  max_length=100)

class DeleteProductForm(forms.Form):
    idproduct = forms.IntegerField(label="idproduct")