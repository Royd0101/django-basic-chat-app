from django.urls import path
from .views import chat_view

urlpatterns = [
    path("chat/<int:receiver_id>/", chat_view, name="chat"),
]
