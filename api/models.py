from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)
    category_image = models.TextField()

    class Meta:
        managed = False
        db_table = 'categories'


class Colors(models.Model):
    color_id = models.CharField(primary_key=True, max_length=15)
    color_name = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'colors'


class Deliveries(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    delivery_date = models.DateField()
    delivery_price = models.IntegerField()
    delivery_status = models.CharField(max_length=12)
    delivery_descrip = models.CharField(max_length=280, blank=True, null=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'deliveries'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField()
    order_status = models.CharField(max_length=12)
    order_ammount = models.IntegerField()
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'orders'


class ProductColor(models.Model):
    product = models.OneToOneField('Products', models.DO_NOTHING, primary_key=True)
    color = models.ForeignKey(Colors, models.DO_NOTHING)
    color_stock = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_color'
        unique_together = (('product', 'color'),)


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=30)
    product_price = models.IntegerField()
    product_stock = models.IntegerField()
    product_image = models.CharField(max_length=200, blank=True, null=True)
    product_descrip = models.CharField(max_length=300, blank=True, null=True)
    product_details = models.CharField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products'

class Images_products(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=30)
    image_text = models.TextField()
    product = models.ForeignKey(Products, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'images_products'


class Sales(models.Model):
    product = models.OneToOneField(Products, models.DO_NOTHING, primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    sale_quantity = models.SmallIntegerField()
    sale_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sales'
        unique_together = (('product', 'order'),)


class Size(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'size'

class Product_size(models.Model):
    product = models.OneToOneField(Products, models.DO_NOTHING, primary_key=True)
    size = models.ForeignKey(Size, models.DO_NOTHING)
    size_stock = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_size'
        unique_together = (('product', 'size'),)



class Users(AbstractUser):
    userid = models.AutoField(primary_key=True)
    usermail = models.CharField(max_length=30,unique=True)
    username = models.CharField(max_length=30,unique=True)
    password_user = models.CharField(max_length=256)
    userphone = models.CharField(max_length=12, blank=True, null=True)
    userrole = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name' , 'last_name'] 


class UserLog(models.Model):
    id = models.IntegerField(primary_key=True)
    token = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'userlog'