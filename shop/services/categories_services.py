from shop.models import Category, SubCategory


def get_subcategories(model_slug):
    category = Category.objects.get(slug=model_slug)
    categories = SubCategory.objects.filter(super_category=category.pk)

    return categories
