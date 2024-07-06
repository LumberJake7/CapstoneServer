from flask import Blueprint, render_template, session, request, flash, redirect
import requests
from models import Menu

search = Blueprint('search', __name__)

API_KEY = '0a6d6c9f43cc45f4a8ac20b49d8d36fd'

@search.route('/search/ingredients', methods=['GET', 'POST'])
def ingredient_search():
    if 'user_id' not in session:
        flash("You must login or create an account to see this page")
        return redirect('/login')
    
    if request.method == 'POST':
        ingredients = [ingredient for ingredient in request.form.getlist('ingredients[]') if ingredient.strip()]
        ignore_pantry = 'true' if request.form.get('ignorePantry') else 'false'
        
        if ingredients:
            ingredients_str = ','.join(ingredients)
            api_url = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}&ingredients={ingredients_str}&number=5&ignorePantry={ignore_pantry}'
            
            response = requests.get(api_url)
            results = response.json()
            
            filtered_results = [recipe for recipe in results if recipe['title'] not in ['Beverages', 'Smoothies']]
            
            return render_template('ingredients.html', results=filtered_results)
    
    return render_template('ingredients.html')


@search.route('/search/details/<int:recipe_id>', methods=['GET'])
def results(recipe_id):
    if 'user_id' not in session:
        flash("You must login or create an account to see this page")
        return redirect('/login')
    
    user_menu_ids = [menu.recipe_id for menu in Menu.query.filter_by(user_id=session['user_id']).all()]
    image_request = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
    summary_request = f'https://api.spoonacular.com/recipes/{recipe_id}/summary?apiKey={API_KEY}'
    instruction_request = f'https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={API_KEY}'

    sum_response = requests.get(summary_request)
    inst_response = requests.get(instruction_request)
    image_response = requests.get(image_request)
    
    if sum_response.status_code == 200 and inst_response.status_code == 200 and image_response.status_code == 200:
        summary = sum_response.json()
        summary_text = summary['summary'].split('With a spoonacular score')[0].strip()
        summary['summary'] = summary_text
        instructions = inst_response.json()
        image_data = image_response.json()

        ingredient_set = set()
        equipment_set = set()
        for instruction in instructions:
            for step in instruction['steps']:
                for ingredient in step['ingredients']:
                    ingredient_set.add(ingredient['name'].capitalize())
                for equipment in step['equipment']:
                    equipment_set.add(equipment['name'].capitalize())

        return render_template("recipeDetails.html", instructions=instructions, summary=summary, image=image_data, user_menu_ids=user_menu_ids, ingredient_set=ingredient_set, equipment_set=equipment_set)
    else:
        return "Failed to retrieve recipe details", 404