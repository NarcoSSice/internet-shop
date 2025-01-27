from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from django.http import JsonResponse
from django.core.cache import cache

from main.settings import RECOMMENDED_SUBCATEGORIES_KEY, RECOMMENDED_PRODUCTS_KEY
from shop.forms import RegisterCustomerForm, LoginUserForm
from shop.models import Shipping

from shop.services.auth_services import confirm_email_customer, confirm_customer
from shop.services.categories_services import get_subcategories, get_product_by_subcategory, get_product
from shop.services.order_services import create_basket_order, create_order_items, create_order_context
from shop.services.AI_services import generate_description, generate_price, generate_image_url
from shop.services.recomended_services import get_recommended_products, get_recommended_subcategories
from shop.services.search_services import recommend_products


def generate_product_description_view(request):
    description = generate_description(request)
    return JsonResponse({'description': description})


def generate_product_price_view(request):
    price = generate_price(request)
    return JsonResponse({'price': price})


def generate_product_image_view(request):
    image_url = generate_image_url(request)
    if type(image_url) is JsonResponse:
        return image_url
    return JsonResponse({'imageUrl': image_url})


def index(request):
    recommended_subcategories = (cache.get(RECOMMENDED_SUBCATEGORIES_KEY)
                                 or get_recommended_subcategories())
    recommended_products = (cache.get(RECOMMENDED_PRODUCTS_KEY)
                            or get_recommended_products(recommended_subcategories.get('subcategories')))
    context = {
        'recommended_subcategories': recommended_subcategories.get('subcategories'),
        'recommended_products': recommended_products.get('products'),
    }
    return render(request, 'shop/base.html', context=context)


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


class MakeOrder(LoginRequiredMixin, CreateView):
    model = Shipping
    fields = ['address', 'city']
    template_name = 'shop/make_order.html'
    login_url = 'my_login'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = create_order_context(self.request)
        context.update(add_context)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)

        order = self.create_order()
        self.create_items(order)

        instance.customer = self.request.user
        instance.order = order
        instance.save()
        return redirect('home')

    def create_order(self):
        user = self.request.user
        return create_basket_order(user)

    def create_items(self, order):
        basket = self.request.session['basket']
        create_order_items(basket, order)


def search_view(request):
    query = request.GET.get('query', '')
    products = recommend_products(query)
    return render(request, 'shop/search.html', {'products': products})
