from django.urls import reverse
from .forms import RegisterForm
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('authors:create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso.')
        del(request.session['register_form_data'])  # noqa E275

    return redirect('authors:register')
