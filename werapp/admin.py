from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from werapp.models import Player

admin.site.register(Player, UserAdmin)
