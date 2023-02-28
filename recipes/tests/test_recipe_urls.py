from django.test import TestCase
from django.urls import reverse


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
