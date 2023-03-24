from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password_confirm = forms.CharField(
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
        labels = {
            'first_name': 'Primeiro nome:',
            'last_name': 'Último nome:',
            'username': 'Nome de usuário:',
            'email': 'E-mail:',
            'password': 'Senha:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Ex.: John',
                'class': 'placeholder-text',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Ex.: Doe',
                'class': 'placeholder-text',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Ex.: john_doe',
                'class': 'placeholder-text',
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Ex.: johndoe@john.com',
                'class': 'placeholder-text',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha',
                'class': 'placeholder-text',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError({
                'password': 'As senhas não conferem, por favor tente novamente.',  # noqa E501
                'password_confirm': 'As senhas não conferem, por favor tente novamente.',  # noqa E501
            })
