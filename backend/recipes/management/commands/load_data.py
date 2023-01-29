import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Начало загрузки данных'))
        with open(
                'data/ingredients.json', encoding='utf-8'
        ) as ingredients_json_data:
            ingredients_data = json.loads(ingredients_json_data.read())
            for ingredients in ingredients_data:
                Ingredient.objects.get_or_create(**ingredients)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
