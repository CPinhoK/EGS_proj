from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories', views.categories, name='categories'),
    path('search/',views.productssearch, name='search'),
    path('products/<product_id>',views.item, name='item'),
    path('addproducts', views.addproductpage, name='addproducts'),
    path('checkout', views.checkout, name='checkout'),
    path('bug', views.addproductform, name='bug'),
    path('addedproduct', views.addproductform, name='addedproduct')
]
