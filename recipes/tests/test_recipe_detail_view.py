from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
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
