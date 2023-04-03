import re
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
