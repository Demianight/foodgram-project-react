from django.contrib import admin

from .models import Favourite, ShoppingCart


class FavouriteAdmin(admin.ModelAdmin):
    pass


class ShoppingCartAdmin(admin.ModelAdmin):
    pass


admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
