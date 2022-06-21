from django.shortcuts import render
from . import forms
import requests
import json

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
        # object_list = list(filter(lambda product: searchquery in product, products))
        temp = json.dumps(products)
        object_list = json.loads(temp)
        output_dict = [product for product in object_list if product['name']==('searchquery')]
        print("Object list: ", output_dict)
        return render(request, 'search.html', {'products': output_dict})

def item(request, product_id):
    request.POST.get('product_id')
    url = 'http://127.0.0.1:8000/products/?id=' + product_id
    product = requests.get(url).json()
    print(product)
    return render(request, 'item.html', {'product': product})

#pagina adicionar produto
def addproductpage(request):
    print("PAGINA ADD PRODUTO")
    return render(request, 'addproduct.html')

    
def addproductform(request):
    print("FORM ADICIONAR PRODUTO")
    try:
        nameproduct = ''
        priceproduct = ''
        imageproduct = ''
        categoryproduct = ''
        statusproduct = ''
        form = forms.AddProductForm(request.POST or None)
        #print(form)
        if form.is_valid():
            print(" Form is valid")
            nameproduct = form.changed_data.get(nameproduct)
            print(nameproduct)
            priceproduct = form.changed_data.get(priceproduct)
            imageproduct = ''
            categoryproduct = form.changed_data.get(categoryproduct)
            statusproduct = form.changed_data.get(statusproduct)
            addproductrequest(nameproduct,priceproduct,imageproduct,categoryproduct,statusproduct)
            print(addproductrequest)
        context = {'form': form, 'nameproduct': nameproduct, 'priceproduct': priceproduct, 'imageproduct': imageproduct, 'categoryproduct': categoryproduct, 'statusproduct': statusproduct}
        return render(request, 'addedproduct.html', context) 
    except:
        print("API stock not working")
        return render(request,'notworking.html')

#pedido adicionar produto
def addproductrequest(self, nameproduct=None, priceproduct=None, imageproduct=None, categoryproduct=None, statusproduct=None):
    print("REQUEST ADICIONAR PRODUTO")
    url = 'http://127.0.0.1:8000/products/'
    headers={ "accept": "*/*",
              "Content-Tyoe": "application/json"}
    data ={ "nameproduct": nameproduct,
            "priceproduct" : priceproduct,
            "imageproduct" : imageproduct,
            "categoryproduct" : categoryproduct,
            "statusproduct" :statusproduct
    }
    addproductreq = requests.post(url,data=json.dumps(data), headers=headers)
    print("API request status code:")
    print(addproductreq.status_code)
    print("API request details:")
    print(addproductreq)
    return addproductreq.json()
        
def checkout(request):
    return render(request, 'checkout.html')

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