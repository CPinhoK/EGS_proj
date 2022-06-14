from doctest import NORMALIZE_WHITESPACE
from itertools import product
from pyexpat import model
from django.db import models
# Create your models here.

###########
# Product #
###########
# class Product(models.Model):
#     product_id = models.AutoField(primary_key=True)
#     name = models.TextField(blank=False, unique=False)
#     photo = models.ImageField(upload_to="./static/img/products/", blank=True, default='static/img/products/product_default.jpg')
#     category = models.TextField(blank=False)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=0.00)

#     def __str__(self):
#         return self.name


# # Each cart item
# class orderItem(models.Model):
#     product = models.IntegerField(blank=False)
#     quantity = models.IntegerField(default=1)

#     def __str__(self):
#         return self.product

# # All cart
# class order(models.Model):
#     cart = models.ManyToManyField(product)
#     user = models.TextField()
#     start_date = models.DateTimeField(auto_now_add=True)
#     ordered_date = models.DateTimeField()
#     ordered = models.BooleanField(default=False)

#     def __str__(self):
#         return self.cart