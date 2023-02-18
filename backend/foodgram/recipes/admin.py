from django.contrib import admin

from .models import Ingredient, Recipe, Tag, IngredientAmount


class Adm(admin.ModelAdmin):
    pass


class RecipeAdmin(Adm):
    pass


class TagAdmin(Adm):
    pass


class IngredientAdmin(Adm):
    pass


class IngredientAmountAdmin(Adm):
    pass


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
