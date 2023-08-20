from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    fields = ["user", "avatar"]


admin.site.register(Profile, ProfileAdmin)
