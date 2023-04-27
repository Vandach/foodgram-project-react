from django.db.models import F, Sum

from .models import RecipeIngredients

def recipe_ingredient_create(ingredients_data, models, recipe):
    bulk_create_data = (
                    models(
                        recipe=recipe,
                        ingredient=ingredient_data['ingredient'],
                        amount=ingredient_data['amount']
                        )
                    for ingredient_data in ingredients_data
    )
    models.objects.bulk_create(bulk_create_data)


def get_list_ingredients(user):
    """
    Cуммирование позиций из разных рецептов.
    """

    ingredients = RecipeIngredients.objects.filter(
        recipe__shopping_recipe__user=user).values(
        name=F('ingredient__name'),
        measurement_unit=F('ingredient__measurement_unit')
    ).annotate(amount=Sum('amount')).values_list(
        'ingredient__name', 'amount', 'ingredient__measurement_unit')
    return ingredients