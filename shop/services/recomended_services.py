import os
import openai
import ast
import random
from django.core.cache import cache
from main.settings import RECOMMENDED_PRODUCTS_KEY, RECOMMENDED_SUBCATEGORIES_KEY
from datetime import datetime
from shop.models import Product, SubCategory

api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)


def get_subcategories():
    subcategory_names = list(SubCategory.objects.values_list('name', flat=True))
    return subcategory_names


def get_season():
    month = int(datetime.now().month)
    if 4 < month < 10:
        return "Тепла пора року"
    return "Холодна пора року"


def get_recommended_products(recommended_subcategories):
    random_category = random.choice(recommended_subcategories)
    subcategory = SubCategory.objects.filter(name=random_category).first()
    products = (
        Product.objects
        .select_related('subcategory__super_category')
        .filter(subcategory=subcategory)
        .order_by('?')[:3]
    )

    cache.set(RECOMMENDED_PRODUCTS_KEY, {'products': products}, timeout=86400)
    return {'products': products}


def get_recommended_subcategories():
    prompt = (
        f"Пора року: {get_season()}. Категорії: {', '.join(get_subcategories())}. "
        f"Які з цих категорій є найактуальнішими для рекомендацій користувачам? "
        f"В відповіді надішли лише список с 3-х категорій у форматі ['Категорія 1', 'Категорія 2', 'Категорія 3']"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ти підбираєш категорії за порою року"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
        )

        ai_recommended = response.choices[0].message.content
        recommended = list(SubCategory.objects.select_related('super_category')
                           .filter(name__in=ast.literal_eval(ai_recommended.strip())))

        cache.set(RECOMMENDED_SUBCATEGORIES_KEY, {'subcategories': recommended}, timeout=86400)
        return {'subcategories': recommended}
    except openai.OpenAIError as e:
        print(e)
        return []
