from django.db import models

class ReceiveOrder(models.Model):
    receive_id = models.AutoField(primary_key=True)
    receive_no = models.CharField(max_length=10)
    receive_date=models.DateTimeField()
    receive_vendor=models.IntegerField()
    receive_amount=models.IntegerField()

class ReceiveOrderDetail(models.Model):
    receive_detail_id=models.AutoField(primary_key=True)
    receive_id=models.IntegerField()
    product_id=models.IntegerField()
    qty=models.IntegerField()
    cost=models.DecimalField()
    po=models.CharField(max_length=10)

class DeliveryOrder(models.Model):
    delivery_id=models.AutoField(primary_key=True)
    delivery_no=models.CharField(max_length=10)
    delivery_date=models.DateTimeField()
    customer_id=models.IntegerField()

class DeliveryOrderDetail(models.Model):
    delivery_detail_id=models.AutoField(primary_key=True)
    delivery_id=models.IntegerField()
    product_id=models.IntegerField()
    qty=models.IntegerField()
    price=models.DecimalField()
    so=models.CharField(max_length=10)
    delivery_recieve_id=models.IntegerField()

class DeliveryOrderDetailReceiveUpdate(models.Model):
    delivery_recieve_id=models.AutoField(primary_key=True)
    sum_of_delivery_detail_qty=models.IntegerField()

class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    product_cost=models.DecimalField()
    product_price=models.DecimalField()

class Vendor(models.Model):
    vendor_id=models.AutoField(primary_key=True)
    vendor_name=models.CharField(max_length=50)

class Customer(models.Model):
    customer_id=models.AutoField(primary_key=True)
    customer_short_name=models.CharField(max_length=50)
    customer_full_name=models.CharField(max_length=150)
    customer_addr1=models.CharField(max_length=200)
    customer_addr2=models.CharField(max_length=200)