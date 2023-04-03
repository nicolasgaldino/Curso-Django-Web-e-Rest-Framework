from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={'required': 'Por favor, digite seu nome de usuário'},
        label='Nome de usuário:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: john_doe',
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
        )
