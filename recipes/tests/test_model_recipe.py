from parameterized import parameterized
from unittest import skip
from django.core.exceptions import ValidationError
from .test_recipe_base import RecipeTestBase, Recipe


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Category'),
            author=self.make_author(username='Nícolas Galdino'),
            title='Test Testado',
            description='Testando meus testes',
            slug='test-testado',
            preparation_time=10,
            preparation_time_unit='Minutos',
            preparation_steps='Recipe Preparation Steps',
            servings=10,
            servings_unit='Pessoas',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand(
        [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ]
    )
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @skip("WIP")
    def test_recipe_preparation_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_is_html)

    @skip("WIP")
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe),
            'Testing Representation'
        )
