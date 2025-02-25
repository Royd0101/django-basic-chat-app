from django.shortcuts import render
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .models import *
# Create your views here.


class Car_view(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializers


class Rental_view(ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializers

def car(request):
    return render(request, 'api/car.html')

def rental(request):
    return render(request, 'api/rental.html')