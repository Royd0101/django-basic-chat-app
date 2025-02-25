from rest_framework import serializers
from .models import *

class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
class RentalSerializers(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    class Meta:
        model = Rental
        fields = ('id', 'car', 'customer_name', 'rental_date', 'return_date')
