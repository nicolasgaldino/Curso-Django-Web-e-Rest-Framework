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

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abcde'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Por favor, verifique sua senha. Certifique-se que ela tenha pelo menos 8 caracteres, com letras maiúsculas, minúsculas e números.'  # noqa E501
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '22565721aA!@'
        self.form_data['password_confirm'] = '22565g721aA!@'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'As senhas não conferem, por favor tente novamente.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_send_get_request_to_regristration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_if_email_already_exists_in_data_base(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Informe um endereço de email válido.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('email'))

    def test_author_created_login(self):
        url = reverse('authors:create')

        self.form_data.update({
            'first_name': 'first',
            'last_name': 'last',
            'username': 'testuser',
            'email': 'user@tester.com',
            'password': '22565721aA!@',
            'password_confirm': '22565721aA!@',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='22565721aA!@'
        )

        self.assertTrue(is_authenticated)
