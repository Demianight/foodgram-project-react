from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime as dt

from recipes.models import IngredientAmount, Recipe
from users.models import User


@dataclass
class IngredientData:
    name: str
    amount: float
    units: str


def make_cart_file(user: User):
    recipes: OrderedDict[Recipe] = user.shopping_cart.all()

    ingredients: list[IngredientData] = []
    for recipe in recipes:
        for ingredient in recipe.ingredients.all():
            amount = IngredientAmount.objects.get(
                recipe=recipe,
                ingredient=ingredient
            ).amount
            data = IngredientData(
                ingredient.name, amount, ingredient.measurement_unit
            )
            # If item does not appear in list 'index' method returns -1
            # To turn it to False statement we just need to add 1 to it
            # So this +1 in 'if' just check duplicates in list
            try:
                index = ingredients.index(data)
                ingredients[index].amount += data.amount
            except ValueError:
                ingredients.append(data)

    date = dt.date(dt.now())
    filename = f'media/shopping_lists/{user.username}_{date}.txt'

    with open(filename, 'w', encoding='utf-8') as f:
        for data in ingredients:
            f.write(f'{data.name}: {data.amount} {data.units}\n')

    return filename
