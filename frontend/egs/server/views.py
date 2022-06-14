from django.shortcuts import render
from . import forms
import requests

#import requests, order, orderItem
#from frontend.egs.server.models import orderItem

# Create your views here.
def index(request):
    products = requests.get('http://127.0.0.1:8000/products').json()
    # returns last 4 products of array to get the newest to index page
    latest = products[-4:]
    return render(request, 'index.html', {'latest': latest})

def categories(request):
    return render(request, 'categories.html')

def productssearch(request):
    #searchquery = forms.SearchForm(request.GET)
    products = requests.get('http://127.0.0.1:8000/products').json()
    print(products)
    searchquery = request.GET.get('querysearch') 
    if searchquery=='':
        print("FORM empty query: " , searchquery)
        return render(request, 'search.html', {'products': products})
    #query está vazia
    else:
        print("FORM VALID query: " , searchquery)
        object_list = list(filter(lambda product: searchquery in product, products))
        print("Object list: ", object_list)
        return render(request, 'search.html', {'products': object_list})

def item(request, product_id):
    request.POST.get('product_id')
    url = 'http://127.0.0.1:8000/products/?id=' + product_id
    product = requests.get(url).json()
    print(product)
    return render(request, 'item.html', {'product': product})

def addproduct(request):
    return render(request, 'addproduct.html')
        

# def addtocart(request,slug):
#     item = get_object_or_404(item, slug=slug)
#     order_item = orderItem.objects.create(item=item)
#     # checks if has an order
#     order_qs = order.objects.filter(user=request.user, ordered=False)
#     #if the order item is in the order
#     if order_qs.exists():
#         order = order_qs[0]
#         if(order.items.filter(item__slug=item.slug).exists()):
#             order_item.quantity +=1
#             order_item.save()
#     else:
#         order = order.objects.create(user=request.user)
#         order.items.add(order_item)

#     return 