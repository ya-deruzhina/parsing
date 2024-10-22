from django.db import models

class ProductModel (models.Model):
    id = models.IntegerField(primary_key=True)
    name_product = models.CharField(max_length=200,null=True)
    type_product = models.CharField(max_length=100,null=True)
    root_type_product = models.CharField(max_length=50,null=True)
    vendor_code = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    color = models.CharField(max_length=50,null=True)
    contents = models.TextField(null=True)
    brand_name = models.CharField(max_length=100,null=True)
    price_without_nds = models.FloatField(null=True)
    price = models.FloatField(null=True)
    options = models.TextField(null=True)
