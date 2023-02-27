from users.models import User


def make_cart_file(user: User):
    ingr_values = user.shopping_cart.values_list(
        'amount__ingredient__id',
        'amount__ingredient__name',
        'amount__ingredient__measurement_unit',
        'amount__amount',
    )
    id = 0
    name = 1
    units = 2
    amount = 3

    result_dict = {}
    for ingredient in ingr_values:
        ingr_id = ingredient[id]
        if ingr_id not in result_dict:
            result_dict[ingr_id] = {
                'name': ingredient[name],
                'measurement_unit': ingredient[units],
                'amount': ingredient[amount],
            }
        else:
            result_dict[ingr_id]['amount'] += ingredient[amount]

    return result_dict
