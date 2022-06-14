from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories', views.categories, name='categories'),
    path('search/',views.productssearch, name='search'),
    path('products/<product_id>',views.item, name='item'),
    path('addproducts', views.addproduct, name='addproducts')
]
