from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from shop.forms import RegisterCustomerForm, LoginUserForm
from shop.services.auth_services import confirm_email_customer, confirm_customer
from shop.services.categories_services import get_subcategories, get_product_by_subcategory, get_product


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


def show_subcategories(request, category_slug):
    subcategories = get_subcategories(category_slug)

    context = {
        'subcategories': subcategories,
    }

    return render(request, 'shop/subcategories.html', context=context)


def show_subcategory_products(request, category_slug, subcategory_slug):
    products, subcategory = get_product_by_subcategory(subcategory_slug)

    context = {
        'products': products,
        'subcategory': subcategory
    }

    return render(request, 'shop/show_subcategory.html', context=context)


def show_products(request, category_slug, subcategory_slug, product_slug):
    product = get_product(product_slug)

    context = {
        'product': product,
    }

    return render(request, 'shop/product_detail.html', context=context)
