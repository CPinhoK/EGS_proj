from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    products = requests.get('http://127.0.0.1:8000/products').json()
    # returns last 4 products of array to get the newest to index page
    latest = products[-4:]
    return render(request, 'index.html', {'latest': latest})

def categories(request):
    return render(request, 'categories.html')

def productssearch(request):
    products = requests.get('http://127.0.0.1:8000/products').json()
    return render(request, 'search.html', {'products': products})

def item(request, product_id):
    request.POST.get('product_id')
    url = 'http://127.0.0.1:8000/products/' + product_id
    product = requests.get(url).json()
    print(product)
    return render(request, 'item.html', {'product': product})