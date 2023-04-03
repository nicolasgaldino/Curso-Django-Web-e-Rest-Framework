import time
from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_the_test(self):
        self.browser.get(self.live_server_url)
        body_html = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Não há receitas cadastradas. Cadastre uma receita aqui.', body_html.text)  # noqa E501
