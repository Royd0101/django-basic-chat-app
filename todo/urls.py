from django.urls import path
from .views import *

urlpatterns = [
    path('import_todo/', import_todo, name='import_todo'),
    path('todo_list/', todo_list, name='todo_list'),
    path('todo_list1/', todo_list1, name='todo_list1'),
]
