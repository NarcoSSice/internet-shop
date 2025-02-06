from django.utils.text import slugify
from unidecode import unidecode


class SlugMixin:
    def create(self, validated_data):
        validated_data['slug'] = slugify(unidecode(validated_data.get('name')))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.slug = slugify(unidecode(validated_data.get('name', instance.name)))
        return super().update(instance, validated_data)
