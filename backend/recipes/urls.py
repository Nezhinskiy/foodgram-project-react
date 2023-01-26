from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'recipes'

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
