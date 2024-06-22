from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('create/', views.recipe_create, name='recipe_create'),
    path('<int:recipe_id>/update/', views.recipe_update, name='recipe_update'),
    path('<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
]