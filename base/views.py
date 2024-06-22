from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Recipe
from .forms import RecipeForm

def recipe_list(request):
    response = requests.get('https://www.themealdb.com/api/json/v1/1/search.php?s=')
    if response.status_code == 200:
        recipes = response.json().get('meals', [])
        recipes = [recipe for recipe in recipes if recipe.get('idMeal')]
        return render(request, 'base/recipe_list.html', {'recipes': recipes})
    else:
        return render(request, 'base/error.html', {'error_message': 'Failed to fetch recipes from API'})


def recipe_detail(request, recipe_id):
    api_endpoint = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={recipe_id}"
    response = requests.get(api_endpoint)

    if response.status_code == 200:
        data = response.json()
        if data["meals"]:
            recipe = data["meals"][0]

            ingredients = []
            for i in range(1, 21):
                ingredient = recipe.get(f'strIngredient{i}')
                measure = recipe.get(f'strMeasure{i}')
                if ingredient:
                    ingredients.append((ingredient, measure))

            return render(request, 'base/detail.html', {'recipe': recipe, 'ingredients': ingredients})
    return render(request, 'base/error.html')

def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'base/create.html', {'form': form})

def recipe_update(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('detail', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'base/update.html', {'form': form, 'recipe': recipe})

def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    return redirect('recipe_list')

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'base/index.html', {'recipes': recipes})
