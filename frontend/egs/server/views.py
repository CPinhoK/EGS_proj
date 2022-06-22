from django.shortcuts import render, redirect
from . import forms
import requests
import json

#import requests, order, orderItem
#from frontend.egs.server.models import orderItem

# Create your views here.
##############
# Index page #
##############
def index(request):
    try:
        token = request.GET.get('token')
        user = request.GET.get('user')
        print("token: ", token)
        print("user: ", user)
        products = requests.get('http://tista-stockapi.egs/products').json()
        print(products)
        if(products!= []):
            # returns last 4 products of array to get the newest to index page
            latest = products[-4:]
            return render(request, 'index.html', {'latest': latest})
        else:
            latest = []
            return render(request, 'index.html', {'latest': latest})
    except:
        return render(request,'notworking.html')

###################
# categories page #
###################
def categories(request):
    return render(request, 'categories.html')

################################
# search products in API stock #
################################
def productssearch(request):
    products = requests.get('http://tista-stockapi.egs/products').json()
    searchquery = request.GET.get('querysearch') 
    if searchquery=='':
        print("FORM empty query: " , searchquery)
        return render(request, 'search.html', {'products': products})
    #query não está vazia
    else:
        print("FORM VALID query: " , searchquery)
        temp = json.dumps(products)
        object_list = json.loads(temp)
        output_dict = [product for product in object_list if product['name']==(searchquery)]
        return render(request, 'search.html', {'products': output_dict})

##########################
# get page for each item #
##########################
def item(request, product_id):
    request.POST.get('product_id')
    url = 'http://tista-stockapi.egs/products/?id=' + product_id
    product = requests.get(url).json()
    print(product)
    return render(request, 'item.html', {'product': product})

######################
# Adicionar produtos #
######################
#pagina adicionar produto
def addproductpage(request):
    print("PAGINA ADD PRODUTO")
    return render(request, 'addproduct.html')

# pedido form adicionar produto    
def addproductform(request):
    print("FORM ADICIONAR PRODUTO")
    try:
        idproduct = ''
        nameproduct = ''
        priceproduct = ''
        imageproduct = ''
        categoryproduct = ''
        statusproduct = ''
        form = forms.AddProductForm(request.POST or None)
        #print(form)
        if form.is_valid():
            print(" Form is valid")
            idproduct= form.cleaned_data['idproduct']
            nameproduct = form.cleaned_data['nameproduct']
            priceproduct = form.cleaned_data['priceproduct']
            imageproduct =  form.cleaned_data['imageproduct']
            categoryproduct = form.cleaned_data['categoryproduct']
            statusproduct = form.cleaned_data['statusproduct']
            addproductrequest(idproduct,nameproduct,priceproduct,imageproduct,categoryproduct,statusproduct)
            #print(addproductrequest)
            context = {'form': form, 'idproduct': idproduct, 'nameproduct': nameproduct, 'priceproduct': priceproduct, 'imageproduct': imageproduct, 'categoryproduct': categoryproduct, 'statusproduct': statusproduct}
            return render(request, 'addedproduct.html', context)
        else:
            print("FORM NOT VALID")
            return render(request,'notworking.html')
    except:
        print("API stock not working")
        return render(request,'notworking.html')

#pedido adicionar produto à api
def addproductrequest(idproduct=None, nameproduct=None, priceproduct=None, imageproduct=None, categoryproduct=None, statusproduct=None):
    print("REQUEST ADICIONAR PRODUTO")
    url = 'http://tista-stockapi.egs/products'
    headers={ "accept": "application/json",
              "Content-Type": "application/json"}
    body ={ "id": idproduct,
            "name": nameproduct,
            "price" : priceproduct,
            "image" : imageproduct,
            "category" : categoryproduct,
            "status" :statusproduct
    }
    print("body: ", body)
    addproductreq = requests.post(url,json=body, headers=headers)
    print("API request status code:")
    print(addproductreq.status_code)
    print("API request details:")
    print(addproductreq.content)
    return addproductreq.json()

###################
# APAGAR produtos #
###################
#pagina apagar produto
def deleteproductpage(request):
    print("PAGINA Delete PRODUTO")
    products = requests.get('http://tista-stockapi.egs/products').json()
    print(products)
    return render(request, 'deleteproduct.html',{'products': products})

# pedido form APAGAR produto   
def deleteproductform(request):
    print("FORM delete PRODUTO")
    try:
        idproduct = ''
        form = forms.DeleteProductForm(request.POST or None)
        #print(form)
        if form.is_valid():
            print(" Form is valid")
            idproduct= form.cleaned_data['idproduct']
            deleteproductrequest(idproduct)
        context = {'form': form, 'idproduct': idproduct}
        return render(request, 'deletedproduct.html', context) 
    except:
        print("API stock not working")
        return render(request,'notworking.html')

#pedido delete produto à api
def deleteproductrequest(idproduct=None):
    print("REQUEST Delete PRODUTO")
    url = 'http://tista-stockapi.egs/products'
    new_url = "{}/{}".format(url, idproduct)
    print(new_url)
    headers={ "accept": "application/json"}
    body ={ "id": idproduct}
    print("body: ", body)
    deleteproductreq = requests.delete(new_url,json=body, headers=headers)
    print("API request status code:", deleteproductreq.status_code)
    print("API request details:", deleteproductreq.content)
    print(deleteproductreq.content)
    return deleteproductreq.json()

######################
# página de checkout #
######################   
# pagina checkout
def checkout(request):
    return render(request, 'checkout.html')

#pedido pagamento à api
def pedidopayment(request, wallet_id):
    print("Pedido pagamento")
    url = 'https://zppinho-papi.egs/payment?wallet_id=' + wallet_id
    response = request.post(url)
    return response

# redirect frontend da pagamento api
def redirectpaymentapi(request):
    url = 'http://zppinho-preact.egs/redirect?url=//spiders-frontend.egs/checkout'
    return redirect(url)

###############
# log in data #
###############
def login(request):
    url="http://hugom.egs/login?redirectUrl=//spiders-frontend.egs/"
    responsepost = requests.get("http://hugom.egs/login?redirectUrl=//spiders-frontend.egs/")
    headerslog = responsepost.headers
    print("headerslog: ",headerslog)
    response = redirect(url)
    print(response)
    return response

###############
# signup data #
###############
def signup(request):
    url="http://hugom.egs/signup?redirectUrl=//spiders-frontend.egs/"
    response = redirect(url)
    print(response)
    return response

def signedup(request):
    pass

###############
# update user #
###############
def updateuser(request):
    url="http://hugom.egs/login?redirectUrl=//spiders-frontend.egs/"
    response = redirect(url)
    print(response)
    return response


#####################
# adicionar ao cart #
#####################

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

