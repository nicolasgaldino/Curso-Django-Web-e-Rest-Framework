from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


def label_tester(self, label_value_test, label_value):
    form = RegisterForm()
    label = form[label_value].field.label.capitalize()
    return self.assertEqual(label_value_test, label)


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
    def test_label_placeholder(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label.capitalize()
        self.assertEqual(label, current_label)
