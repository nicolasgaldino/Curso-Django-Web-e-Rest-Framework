import pytest
from unittest.mock import patch
from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body_html = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Não há receitas cadastradas. Cadastre uma receita aqui.', body_html.text)  # noqa E501

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = "É disso que eu preciso!"

        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Usuário vê um campo de busca com o texto "Busque por uma receita..."
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Busque por uma receita..."]'
        )

        # usuário clica no input e busca por uma receita
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            title_needed,
            self.browser.find_element(By.TAG_NAME, 'body').text,
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Usuário vê que tem paginação e clica na página 2
        self.browser.find_element(
            By.XPATH,
            '//nav[@aria-label="Pagination"]'
        )

        self.sleep()
