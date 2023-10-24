from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from shop.forms import RegisterCustomerForm, LoginUserForm
from shop.services.auth_services import confirm_email_customer, confirm_customer


def index(request):
    return render(request, 'shop/base.html')


class RegisterView(FormView):
    form_class = RegisterCustomerForm
    template_name = 'shop/auth/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        confirm_email_customer(self.request, form)
        return super().form_valid(form)


def register_confirm(request, token):
    result = confirm_customer(token)
    if result:
        return redirect(to=reverse_lazy('home'))
    return redirect(to=reverse_lazy('register'))


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'shop/auth/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_customer(request):
    logout(request)
    return redirect('home')
