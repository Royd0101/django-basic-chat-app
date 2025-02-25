from django.urls import path
from .views import *

urlpatterns = [
    path("chat/<int:receiver_id>/", chat_view, name="chat"),
    path("friends/send/<int:receiver_id>/", send_friend_request, name="send_friend_request"),
    path("friends/accept/<int:request_id>/", accept_friend_request, name="accept_friend_request"),
    path("friends/reject/<int:request_id>/", reject_friend_request, name="reject_friend_request"),
    path("friends/", friend_list, name="friend_list"),
]
