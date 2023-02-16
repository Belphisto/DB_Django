from email.policy import default
from statistics import mode
from unicodedata import decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Manga(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    price = models.FloatField(validators=[MinValueValidator(0)])

class User(models.Model):
    name = models.CharField(max_length=30)
    login = models.CharField(max_length=30, unique=True)
    role = models.IntegerField(validators=[MinValueValidator(0)])
    password = models.CharField(max_length=16)
    mail = models.EmailField(max_length=254)

class Order(models.Model):
    name = models.CharField(max_length=30)
    login = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
    
    def get_total_cost(self):
        summ = sum(item.get_cost() for item in self.items.all())
        summ = round(summ, 2)
        return summ

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name = 'items', on_delete = models.CASCADE)
    manga = models.ForeignKey(Manga, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        tmp = self.price*self.quantity
        tmp = round(tmp, 2)
        return tmp