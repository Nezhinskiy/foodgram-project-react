from django.contrib import admin

from recipes import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Администрирование рецептов.
    """
    list_display = ('name', 'id', 'author', 'text', 'image')
    list_filter = ('author', 'name', 'tags')


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Администрирование ингредиентов.
    """
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Администрирование тегов.
    """
    list_display = ('name', 'color', 'slug')


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    Администрирование добавления рецептов в избранное.
    """
    list_display = ('user', 'recipe')


@admin.register(models.IngredientInRecipe)
class IngredientInRecipe(admin.ModelAdmin):
    """
    Администрирование ингредиентов в рецептах.
    """
    list_display = ('recipe', 'ingredient', 'amount')
