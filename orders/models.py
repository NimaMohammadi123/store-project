from statistics import mode
from django.db import models
from shop.models import Product
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Order(models.Model):
    first_name = models.CharField(_('first name'),max_length=50)
    last_name = models.CharField(_('last name'),max_length=50)
    email = models.EmailField(_('e-mail'),max_length=254)
    address = models.TextField(_('address'))
    post_address = models.CharField(_('post address'),max_length=50)
    city = models.CharField(_('city'),max_length=250)
    create = models.DateTimeField(_('created'),auto_now_add=True)
    update = models.DateTimeField(_('updated'),auto_now=True)
    paid = models.BooleanField(_('paid'),default=False)
    
    class Meta:
        ordering = ('-create',)
    
    def __str__(self):
        return f'order by {self.id}'
    
    def total_cost(self):
       return sum(items.get_cost() for items in self.item.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order , related_name='item' , on_delete=models.CASCADE)
    product = models.ForeignKey(Product ,related_name='order_item',on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity