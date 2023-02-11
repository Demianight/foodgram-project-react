import csv
from recipes.models import Ingredient


def load_ingrediens():
    with open('../data/ingredients.csv',
              encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            Ingredient.objects.get_or_create(
                name=row[0],
                measurement_unit=row[1],
            )


def run():
    load_ingrediens()