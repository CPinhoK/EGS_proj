from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories', views.categories, name='categories'),
    path('search/',views.productssearch, name='search'),
    path('products/<product_id>',views.item, name='item'),
    path('addproduct', views.addproductpage, name='addproduct'),
    path('deleteproduct', views.deleteproductpage, name='deleteproduct'),
    path('checkout', views.checkout, name='checkout'),
    path('login', views.login, name='login'),
    path('bug', views.addproductform, name='bug'),
    path('addedproduct', views.addproductform, name='addedproduct'),
    path('deletedproduct', views.deleteproductform, name='deletedproduct')
]
