from django.test import TestCase
from recipes.models import Category, Recipe
from django.contrib.auth.models import User


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
            self,
            first_name='Nícolas',
            last_name='Galdino',
            username='nicolas_galdino',
            password='123456',
            email='nicolas@nicolas.com',
            ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
            self,
            category_data=None,
            author_data=None,
            title='Test Testado',
            description='Testando meus testes',
            slug='test-testado',
            preparation_time=10,
            preparation_time_unit='Minutos',
            preparation_steps='Recipe Preparation Steps',
            preparation_is_html=False,
            servings=10,
            servings_unit='Pessoas',
            is_published=True,
            ):

        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            preparation_steps=preparation_steps,
            preparation_is_html=preparation_is_html,
            servings=servings,
            servings_unit=servings_unit,
            is_published=is_published,
        )

    def make_recipe_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            kwargs = {
                'author_data': {'username': f'u{i}'},
                'category_data': {'name': f'n{i}'},
                'title': f'Título da Receita {i}',
                'slug': f'r{i}',
            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
