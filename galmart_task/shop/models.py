from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    open = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    status_types = (
        ("Готовится", "Готовится"),
        ("Доставка", "Доставка"),
        ("Завершен", "Завершен"),
    )
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    status = models.CharField(choices=status_types, max_length=255)
    amount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    def __str__(self):
        return f"{self.id}.     {self.shop.name} - {self.status}"