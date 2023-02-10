from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class AbstractAdminClass(admin.ModelAdmin):
    pass


class RecipeAdmin(AbstractAdminClass):
    pass


class TagAdmin(AbstractAdminClass):
    pass


class IngredientAdmin(AbstractAdminClass):
    pass


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
