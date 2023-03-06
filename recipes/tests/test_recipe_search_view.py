from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_use_correct_view_function(self):
        search_url = resolve(reverse('recipes:search'))
        self.assertIs(search_url.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(
            response,
            'recipes/pages/search.html',
            )

    def test_recipe_search_raises_404_if_not_search_term(self):
        search_url = reverse('recipes:search')
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_apeg_title_and_scaped(self):
        search_url = (reverse('recipes:search') + '?q=Teste')
        response = self.client.get(search_url)
        self.assertIn(
            'Search for &quot;Teste&quot;',
            response.content.decode('utf-8'),
        )
