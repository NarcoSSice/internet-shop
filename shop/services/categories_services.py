from django.shortcuts import get_object_or_404

from shop.models import Category, SubCategory, Product


def get_subcategories(model_slug):
    category = get_object_or_404(Category, slug=model_slug)
    categories = SubCategory.objects.select_related('super_category').filter(super_category=category.pk)

    return categories


def get_product_by_subcategory(subcategory_slug):
    subcategory = SubCategory.objects.select_related('super_category').get(slug=subcategory_slug)
    products = Product.objects.select_related('subcategory__super_category').filter(subcategory=subcategory.pk)

    return products, subcategory


def get_product(product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    return product
