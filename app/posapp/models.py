from django.db import models

# Create your models here.

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    stock_quantity = models.IntegerField(default=1)
    # objects = models.Manager()
    def getPrice(self):
        return self.item_price
    def getName(self):
        return self.item_name
    def __str__(self):
        return str(self.pk) + ": " + self.item_name

class Order(models.Model):
    total_amount_paid = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    order_date = models.DateField(auto_now_add=True)
    payment_choices = [('C','Cash'),
                       ('CR','Credit Card')]
    payment_type = models.CharField(default='C',max_length=255,choices=payment_choices)

class OrderItem(models.Model):
    item_type = models.ForeignKey(to=Item,null=True,on_delete=models.CASCADE)
    order = models.ForeignKey(to=Order,null=True,on_delete=models.CASCADE)
    line_total = models.DecimalField(max_digits=20,decimal_places=2)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.quantity) + " x " + str(self.item_type.item_name)