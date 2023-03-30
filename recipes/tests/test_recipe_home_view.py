from recipes import views
from unittest.mock import patch
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_working(self):
        home_view = resolve(reverse('recipes:home'))
        self.assertIs(home_view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(
            response,
            'recipes/pages/home.html',
        )

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Não há receitas cadastradas.',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        response_content_recipes = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Test Testado', response_content_recipes)
        self.assertIn('10 Minutos', response_content_recipes)
        self.assertIn('10 Pessoas', response_content_recipes)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipe_is_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Não há receitas cadastradas.',
            response.content.decode('utf-8')
        )

    def test_recipe_home_Is_paginated(self):
        for i in range(9):
            kwargs = {
                'author_data': {'username': f'u{i}'},
                'category_data': {'name': f'n{i}'},
                'slug': f'r{i}',
            }
            self.make_recipe(**kwargs)
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 3)

    def test_invalid_page_query_uses_page_one(self):
        for i in range(9):
            kwargs = {
                'author_data': {'username': f'u{i}'},
                'category_data': {'name': f'n{i}'},
                'slug': f'r{i}',
            }
            self.make_recipe(**kwargs)
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=1A')
            self.assertEqual(response.context['recipes'].number, 1)
