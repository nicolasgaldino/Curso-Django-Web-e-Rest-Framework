from django.test import TestCase
from recipes import views
from django.urls import (
    reverse,
    resolve,
)


class RecipeURLsTest(TestCase):
    def test_if_recipe_home_url_is_working(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')

    def test_if_recipe_category_url_is_working(self):
        category_url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(category_url, '/recipes/category/1/')

    def test_if_recipe_recipe_detail_url_is_working(self):
        recipe_detail_url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(recipe_detail_url, '/recipes/1/')


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
