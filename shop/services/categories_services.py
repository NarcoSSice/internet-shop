from django.shortcuts import get_object_or_404

from shop.models import Category, SubCategory, Product


def get_subcategories(model_slug):
    category = get_object_or_404(Category, slug=model_slug)
    categories = SubCategory.objects.filter(super_category=category.pk)

    return categories


def get_product_by_subcategory(subcategory_slug):
    subcategory = SubCategory.objects.get(slug=subcategory_slug)
    products = Product.objects.filter(subcategory=subcategory.pk)

    return products, subcategory
