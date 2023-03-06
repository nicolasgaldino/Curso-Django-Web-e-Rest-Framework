from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
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
