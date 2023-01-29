import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Начало загрузки данных'))
        with open(
                'data/ingredients.json', encoding='utf-8'
        ) as ingredients_json_data:
            ingredients_data = json.loads(ingredients_json_data.read())
            for ingredients in ingredients_data:
                Ingredient.objects.get_or_create(**ingredients)

        with open('data/tags.json', encoding='utf-8') as dtags_json_data:
            tags_data = json.loads(dtags_json_data.read())
            for tags in tags_data:
                Tag.objects.get_or_create(**tags)

        self.stdout.write(self.style.SUCCESS('Данные загружены'))
