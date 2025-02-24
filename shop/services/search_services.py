import os
import openai
import ast
from shop.models import Product

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def get_products():
    result = Product.objects.all()
    sp = []
    for i in result:
        sp.append(i.name)
    return sp


def recommend_products(query):
    products = get_products()
    prompt = (
        f"Користувач шукає '{query}'. Ось список продуктів  {products}"
        f"Напиши всі продукти які підходять запиту. Якщо таких продуктів немає запропонуй аналоги"
        f"Якщо запит не зрозумілий, оптимізуй його на свій розсуд"
        f"У відповіді повинен бути один список у вигляді продуктів ['Продукт 1', 'Продукт 2', 'Продукт ...']."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ти оптимізуєш запити користувачів та обираєш продукти"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        recommendations = response.choices[0].message.content
        start_index = recommendations.find('[')
        res = recommendations[start_index:]
        print(res)
        recommended = list(Product.objects.filter(name__in=ast.literal_eval(res.strip())))
        return recommended
    except openai.OpenAIError as e:
        print(e)
        return []
