from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            Tag)
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор просмотра тегов.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор просмотра ингридиентов.
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиентов в рецепте.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор просмотра рецепта.
    """
    tags = TagSerializer(read_only=False, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True, source='ingredient_list'
    )
    favorites = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'favorites', 'name',
            'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorites(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.favorites.filter(user=request.user).exists()


class CreateRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания рецепта.
    """
    ingredients = IngredientInRecipeSerializer(many=True,)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
        error_messages={'does_not_exist': 'Указанного тега не существует'}
    )
    image = Base64ImageField(max_length=None)
    author = UserSerializer(read_only=True)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time'
        )

    def validate_tags(self, tags):
        for tag in tags:
            if not Tag.objects.filter(id=tag.id).exists():
                raise serializers.ValidationError(
                    'Указанного тега не существует'
                )
        return tags

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Время готовки должно быть не менее одной минуты'
            )
        return cooking_time

    def validate_ingredients(self, ingredients):
        ingredients_list = []
        if not ingredients:
            raise serializers.ValidationError('Отсутствуют ингридиенты')
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError(
                    'Ингридиенты должны быть уникальны'
                )
            ingredients_list.append(ingredient['id'])
            if int(ingredient.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента более 0'
                )
        return ingredients

    @staticmethod
    def create_ingredients(recipe, ingredients):
        ingredient_list = []
        for ingredient_data in ingredients:
            ingredient_list.append(
                IngredientInRecipe(
                    ingredient=ingredient_data.pop('id'),
                    amount=ingredient_data.pop('amount'), recipe=recipe
                )
            )
        IngredientInRecipe.objects.bulk_create(ingredient_list)

    def create(self, validated_data):
        request = self.context.get('request', None)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        instance.tags.set(validated_data.pop('tags'))
        ingredients = validated_data.pop('ingredients')
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    """
    Сериализатор избранных рецептов.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор избранных рецептов.
    """
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        if user.favorites.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт уже был добавлен в избранное.'
            )
        return data

    def to_representation(self, instance):
        return FavoriteRecipesSerializer(
            instance.recipe, context={'request': self.context.get('request')}
        ).data
