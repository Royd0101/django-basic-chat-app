from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ChatMessage)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(UserStatus)