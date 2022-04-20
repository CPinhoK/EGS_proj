from django.db import models
# Create your models here.

###########
# Product #
###########
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False, unique=False)
    photo = models.ImageField(upload_to="./static/img/products/", blank=True, default='static/img/products/product_default.jpg')
    category = models.TextField(blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=0.00)

    def __str__(self):
        return self.name


