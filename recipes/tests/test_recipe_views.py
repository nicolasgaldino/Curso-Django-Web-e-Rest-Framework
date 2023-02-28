from django.test import TestCase
from recipes import views
from django.urls import (
    reverse,
    resolve,
)


class RecipeViewsTest(TestCase):
    # Home View Tests
    def test_recipe_home_view_function_is_working(self):
        home_view = resolve(reverse('recipes:home'))
        self.assertIs(home_view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_correct_template(self):
        template = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(
            template,
            'recipes/pages/home.html',
        )

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Não há receitas cadastradas.',
            response.content.decode('utf-8')
        )
    # Home View Tests

    # Category View Tests
    def test_recipe_category_view_function_is_working(self):
        category_view = resolve(
            reverse(
                'recipes:category',
                kwargs={'category_id': 1},
            )
        )
        self.assertIs(category_view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': 1000},
            )
        )
        self.assertEqual(response.status_code, 404)
    # Category View Tests

    # Recipe Detail View Tests
    def test_recipe_detail_function_is_working(self):
        recipe_detail = resolve(
            reverse(
                'recipes:recipe',
                kwargs={'id': 1},
            )
        )
        self.assertIs(recipe_detail.func, views.recipe)

    def test_recipe_detail_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': 1000},
            )
        )
        self.assertEqual(response.status_code, 404)
    # Recipe Detail View Tests
