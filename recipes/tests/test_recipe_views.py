from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    # Home View Tests
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

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'Category Test'
        self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': 1}
                )
            )
        response_content_recipes = response.content.decode('utf-8')
        self.assertIn(needed_title, response_content_recipes)

    def test_recipe_category_template_dont_load_recipe_is_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': recipe.category.id}
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

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'
        self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': 1}
                )
            )
        response_content_recipes = response.content.decode('utf-8')
        self.assertIn(needed_title, response_content_recipes)

    def test_recipe_detail_template_dont_load_recipe_is_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': recipe.id}
                )
            )
        self.assertEqual(response.status_code, 404)
    # Recipe Detail View Tests

    # Recipe Search View Tests
    def test_recipe_search_use_correct_view_function(self):
        search_url = resolve(reverse('recipes:search'))
        self.assertIs(search_url.func, views.search)
    # Recipe Search View Tests
