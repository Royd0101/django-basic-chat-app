from django.db import models

# Create your models here.

class Car(models.Model):
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.make} {self.model} {self.year}"


class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    rental_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.customer_name if self.customer_name else "Unnamed Rental"


