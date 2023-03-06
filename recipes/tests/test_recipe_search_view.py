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

    def test_recipe_search_can_find_recipe_by_title(self):
        frst_title = 'This is recipe one'
        scnd_title = 'This is recipe two'

        frst_recipe = self.make_recipe(
            category_data={'name': 'one'},
            slug='one',
            title=frst_title,
            author_data={'username': 'one'}
        )

        scnd_recipe = self.make_recipe(
            category_data={'name': 'two'},
            slug='two',
            title=scnd_title,
            author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        frst_response = self.client.get(f'{search_url}?q={frst_title}')
        scnd_response = self.client.get(f'{search_url}?q={scnd_title}')
        both_response = self.client.get(f'{search_url}?q=this')

        self.assertIn(frst_recipe, frst_response.context['recipes'])
        self.assertNotIn(scnd_recipe, frst_response.context['recipes'])

        self.assertIn(scnd_recipe, scnd_response.context['recipes'])
        self.assertNotIn(frst_recipe, scnd_response.context['recipes'])

        self.assertIn(frst_recipe, both_response.context['recipes'])
        self.assertIn(scnd_recipe, both_response.context['recipes'])

    def test_recipe_search_can_find_recipe_by_description(self):
        frst_descriptiom = 'This is recipe one'
        scnd_description = 'This is recipe two'

        frst_recipe = self.make_recipe(
            category_data={'name': 'one'},
            slug='one',
            description=frst_descriptiom,
            author_data={'username': 'one'}
        )

        scnd_recipe = self.make_recipe(
            category_data={'name': 'two'},
            slug='two',
            description=scnd_description,
            author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        frst_response = self.client.get(f'{search_url}?q={frst_descriptiom}')
        scnd_response = self.client.get(f'{search_url}?q={scnd_description}')
        both_response = self.client.get(f'{search_url}?q=this')

        self.assertIn(frst_recipe, frst_response.context['recipes'])
        self.assertNotIn(scnd_recipe, frst_response.context['recipes'])

        self.assertIn(scnd_recipe, scnd_response.context['recipes'])
        self.assertNotIn(frst_recipe, scnd_response.context['recipes'])

        self.assertIn(frst_recipe, both_response.context['recipes'])
        self.assertIn(scnd_recipe, both_response.context['recipes'])
