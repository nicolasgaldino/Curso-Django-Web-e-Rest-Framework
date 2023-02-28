from django.test import TestCase
from recipes import views
from django.urls import (
    reverse,
    resolve,
)


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_working(self):
        home_view = resolve(reverse('recipes:home'))
        self.assertIs(home_view.func, views.home)

    def test_recipe_category_view_function_is_working(self):
        category_view = resolve(
            reverse(
                'recipes:category',
                kwargs={'category_id': 1},
            )
        )
        self.assertIs(category_view.func, views.category)

    def test_recipe_recipe_view_function_is_working(self):
        recipe_view = resolve(
            reverse(
                'recipes:recipe',
                kwargs={'id': 1},
            )
        )
        self.assertIs(recipe_view.func, views.recipe)
