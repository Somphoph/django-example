from django.db import models


class Product(models.Model):
    def __str__(self):
        return self.product_name

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_cost = models.DecimalField(max_digits=6, decimal_places=2)
    product_price = models.DecimalField(max_digits=6, decimal_places=2)


class Vendor(models.Model):
    def __str__(self):
        return self.vendor_name

    vendor_id = models.AutoField(primary_key=True)
    vendor_name = models.CharField(max_length=50)


class Customer(models.Model):
    def __str__(self):
        return self.customer_full_name

    customer_id = models.AutoField(primary_key=True)
    customer_short_name = models.CharField(max_length=50)
    customer_full_name = models.CharField(max_length=150)
    customer_addr1 = models.CharField(max_length=200)
    customer_addr2 = models.CharField(max_length=200)


class ReceiveOrder(models.Model):
    receive_id = models.AutoField(primary_key=True)
    receive_no = models.CharField(max_length=10)
    receive_date = models.DateTimeField()
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    receive_amount = models.IntegerField()


class ReceiveOrderDetail(models.Model):
    receive_detail_id = models.AutoField(primary_key=True)
    receive_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    po = models.CharField(max_length=10)


class DeliveryOrder(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    delivery_no = models.CharField(max_length=10)
    delivery_date = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class DeliveryOrderDetail(models.Model):
    delivery_detail_id = models.AutoField(primary_key=True)
    delivery_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    so = models.CharField(max_length=10)
    delivery_receive_id = models.IntegerField()


class DeliveryOrderDetailReceiveUpdate(models.Model):
    delivery_receive_id = models.AutoField(primary_key=True)
    sum_of_delivery_detail_qty = models.IntegerField()
