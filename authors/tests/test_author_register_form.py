from django.urls import reverse
from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.test import TestCase as DjangoTestCase


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('username', 'Ex.: john_doe'),
        ('email', 'Ex.: johndoe@john.com'),
        ('password', 'Digite sua senha'),
        ('password_confirm', 'Repita sua senha'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('first_name', 'Primeiro nome:'),
        ('last_name', 'Último nome:'),
        ('username', 'Nome de usuário:'),
        ('email', 'E-mail:'),
        ('password', 'Senha:'),
        ('password_confirm', 'Confirmação de senha:'),
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label.capitalize()
        self.assertEqual(label, current_label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'first_name': 'first',
            'last_name': 'last',
            'username': 'user',
            'email': 'user',
            'password': '22565721aA!@',
            'password_confirm': '22565721aA!@',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('first_name', 'Digite seu primeiro nome'),
        ('last_name', 'Digite seu último nome'),
        ('username', 'Digite seu nome de usuário'),
        ('email', 'Digite seu e-mail'),
        ('password', 'Digite sua senha'),
        ('password_confirm', 'Repita sua senha'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_8(self):
        self.form_data['username'] = 'abcd'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Certifique-se que seu nome de usuário tenha no mínimo 8 caracteres'  # noqa E501
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_100(self):
        self.form_data['username'] = 'a' * 101
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Certifique-se que seu nome de usuário tenha no máximo 100 caracteres'  # noqa E501
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))