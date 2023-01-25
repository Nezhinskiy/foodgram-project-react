from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models import UniqueConstraint

LENGTH_OF_FIELDS_RECIPES = 200

User = get_user_model()


class Ingredient(models.Model):
    """
    Модель ингидиентов.
    """
    name = models.CharField(
        max_length=LENGTH_OF_FIELDS_RECIPES,
        verbose_name='Название инредиента', db_index=True
    )
    measurement_unit = models.CharField(
        max_length=LENGTH_OF_FIELDS_RECIPES, verbose_name='Units'
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """
    Модель тегов.
    """
    name = models.CharField(
        'Название тега', unique=True, max_length=LENGTH_OF_FIELDS_RECIPES
    )
    color = models.CharField(
        'Цвет в HEX-кодировке',
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введенное значение не является цветом в формате HEX'
            )
        ]
    )
    slug = models.SlugField(
        'Уникальный slug', unique=True, max_length=LENGTH_OF_FIELDS_RECIPES,
        db_index=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель рецептов.
    """
    author = models.ForeignKey(
        User, verbose_name='Автор рецептов', on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        'Название рецепта', max_length=LENGTH_OF_FIELDS_RECIPES
    )
    image = models.ImageField(
        upload_to='recipes/image/', verbose_name='Изображение'
    )
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipes', verbose_name='Ингредиенты',
        through='IngredientInRecipe'
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Продолжительность готовки',
        validators=[
            MinValueValidator(
                1, message='Продолжительность готовки не менее 1 минуты'
            ),
            MaxValueValidator(
                300, message='Продолжительность готовки не более 5 часов'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """
    Ингридиенты рецепта.
    """
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredient_list',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, message='Минимальное количество 1!')],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return (
            f'{self.ingredient.name} – {self.amount} '
            f'{self.ingredient.measurement_unit}'
        )


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в избранное "{self.recipe}"'
