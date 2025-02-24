from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

def chat_view(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    return render(request, "chat/chat.html", {"receiver": receiver})
