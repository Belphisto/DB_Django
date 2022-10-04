from statistics import mode
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Manga(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    price = models.FloatField(validators=[MinValueValidator(0)])
