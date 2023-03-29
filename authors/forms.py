import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Por favor, verifique sua senha. Certifique-se que ela '
            'tenha pelo menos 8 caracteres, com letras maiúsculas, '
            'minúsculas e números.'
        ),
            code='Invalid',
        )


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        error_messages={'required': 'Digite seu primeiro nome'},
        label='Primeiro nome:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: John',
            'class': 'placeholder-text',
        })
    )

    last_name = forms.CharField(
        error_messages={'required': 'Digite seu último nome'},
        label='Último nome:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Doe',
            'class': 'placeholder-text',
        })
    )

    username = forms.CharField(
        error_messages={
            'required': 'Digite seu nome de usuário',
            'min_length': 'Certifique-se que seu nome de usuário tenha no mínimo 8 caracteres',  # noqa E501
            'max_length': 'Certifique-se que seu nome de usuário tenha no máximo 100 caracteres',  # noqa E501
            },
        help_text=(
            'Seu nome de usuário deve conter letrar, números ou '
            'um desses caracteres @/./+/-/_ apenas.'
            'O tamanho mínimo para seu nome de usuário é de 8 caracteres '
            'e o máximo é de 100.'
        ),
        label='Nome de usuário:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: john_doe',
            'class': 'placeholder-text',
        }),
        min_length=8, max_length=100,
    )

    email = forms.EmailField(
        error_messages={'required': 'Digite seu e-mail'},
        label='E-mail:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: johndoe@john.com',
            'class': 'placeholder-text',
        })
    )

    password = forms.CharField(
        error_messages={'required': 'Digite sua senha'},
        label='Senha:',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
            'class': 'placeholder-text',
        }),
        validators=[strong_password]
    )

    password_confirm = forms.CharField(
        error_messages={'required': 'Repita sua senha'},
        label='Confirmação de senha:',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita sua senha',
            'class': 'placeholder-text',
        }),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError({
                'password': 'As senhas não conferem, por favor tente novamente.',  # noqa E501
                'password_confirm': 'As senhas não conferem, por favor tente novamente.',  # noqa E501
            })
