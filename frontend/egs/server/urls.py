from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories', views.categories, name='categories'),
    path('search',views.search, name='search'),
    path('item',views.item, name='item'),
]
