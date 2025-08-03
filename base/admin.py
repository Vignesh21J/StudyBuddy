from django.contrib import admin
from .models import Room, Topic, Message, MessageFile

from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'name', 'is_staff', 'is_active']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'bio', 'avatar')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'bio', 'avatar')}),
    )




# Register your models here.

admin.site.register(Room)

admin.site.register(Topic)

admin.site.register(Message)
admin.site.register(MessageFile)
