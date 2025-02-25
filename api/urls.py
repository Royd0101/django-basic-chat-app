from django.urls import path,include

from .views import *

urlpatterns = [
    path('',include([
        #card api
        path('car/', Car_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('car/<int:pk>/', Car_view.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        })),

        #rental api
        path('rental/', Rental_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('rental/<int:pk>/', Rental_view.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),

    path('car_list/', car, name='car_list'),
    path('rental_list/', rental, name='rental_list'),
]