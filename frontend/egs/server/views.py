from django.forms import DateTimeField
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Product

# Create your views here.
def index(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'index.html', {'products': products})

def categories(request):
    return render(request, 'categories.html')

def search(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'search.html', {'products': products})

def item(request):
    return render(request, 'item.html')