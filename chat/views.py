from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import *
from itertools import chain

User = get_user_model()

def chat_view(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    return render(request, "chat/chat.html", {"receiver": receiver})



def send_friend_request(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    
    if request.user == receiver:
        return JsonResponse({"error": "You cannot add yourself as a friend."}, status=400)

    # Check if request already exists
    existing_request = FriendRequest.objects.filter(sender=request.user, receiver=receiver, status="pending").exists()
    if existing_request:
        return JsonResponse({"error": "Friend request already sent."}, status=400)

    # Create friend request
    FriendRequest.objects.create(sender=request.user, receiver=receiver)
    return JsonResponse({"message": "Friend request sent successfully."}, status=200)


def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)

    # Update the request status
    friend_request.status = "accepted"
    friend_request.save()

    # Create a friendship relation
    Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)

    return JsonResponse({"message": "Friend request accepted."}, status=200)


def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)

    friend_request.status = "rejected"
    friend_request.save()

    return JsonResponse({"message": "Friend request rejected."}, status=200)


def friend_list(request):
    friends1 = Friendship.objects.filter(user1=request.user).values_list("user2", flat=True)
    friends2 = Friendship.objects.filter(user2=request.user).values_list("user1", flat=True)

    friends_ids = list(chain(friends1, friends2))
    friends = User.objects.filter(id__in=friends_ids).select_related("status")  # Include status model

    return render(request, "chat/friends_list.html", {"friends": friends})