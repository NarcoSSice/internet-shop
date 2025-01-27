import openai
from main.secret_info import OPENAI_KEY
from django.http import JsonResponse

client = openai.OpenAI(api_key=OPENAI_KEY)


def get_data(request):
    data = {
        'product_name': request.GET.get('product_name'),
        'subcategory': request.GET.get('subcategory')
    }
    return data


def generate_description(request):
    request_data = get_data(request)
    prompt = f"Напиши унікальний опис для товару '{request_data['product_name']}' \
     у категорії '{request_data['subcategory']}'. Треба суцільний текст без ніяких пунктів"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ти експерт з аналізу ринку в Україні."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
        )
        description = response.choices[0].message.content
        return description.strip()
    except openai.OpenAIError as e:
        return JsonResponse({"error": f"Помилка генерації опису: {e}"}, status=400)


def generate_price(request):
    request_data = get_data(request)
    prompt = f"Проаналізуй, яка середня ринкова ціна для '{request_data['product_name']}' в Україні.\
     Вкажи орієнтовну ціну в гривнях, враховуючи сучасні тенденції та доступну інформацію. \
     Відповіддю повине бути лише число"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ти генератор описів товарів."},
                {"role": "user", "content": prompt}
            ]
        )
        market_price = response.choices[0].message.content
        return market_price.strip()
    except openai.OpenAIError as e:
        return JsonResponse({"error": f"Помилка аналізу ціни: {e}"}, status=400)


def generate_image_url(request):
    request_data = get_data(request)
    prompt = f"Згенеруй картинку {request_data['product_name']}"
    try:
        # response = client.images.generate(
        #     model="dall-e-2",
        #     prompt=prompt,
        #     n=1,
        #     size="512x512"
        # )
        # return response.data[0].url
        return 'https://i.postimg.cc/QdGVLLH3/DALL-E-2025-01-17-17-08-27-A-detailed-illustration-of-a-Budweiser-beer-bottle-placed-on-a-wooden-t.png'
    except openai.OpenAIError as e:
        return JsonResponse({"error": f"Помилка генерації картинки: {e}"}, status=400)
