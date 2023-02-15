from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    pass


class FollowAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
