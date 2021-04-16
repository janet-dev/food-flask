"""
Python with 'Flask' & 'pandas'

*****************************************************
Really IMPORTANT...

Make sure you have the following packages installed:
    Flask
    pandas
    request

To check from the PyCharm Terminal pane:
> pip list

For missing libraries, choose & install:
> pip install requests
> pip install flask
> pip install pandas
*****************************************************

Imported 'Flask' & 'request' libraries:
render_template: renders the html templates or pages
is returned in our function

"@app.route('/')"
Runs on local server at http://127.0.0.1:5000/

"@app.route('/cfg')"
Runs on local server at http://127.0.0.1:5000/cfg

Directory/file structure
------------------------
PythonFlask>                'project folder'
        static>             'CSS, images & other files stored in this folder'
            style.css
            my.mp3
        templates>          'HTML web pages stored in this folder
            homepage.html
            page1.html
            page2.html
        venv>               'PyCharm virtual environment
        app.py              'Our web app'

Imported 'pandas' library
'pandas' is a software library written for the Python programming language for data manipulation and analysis.
In particular, it offers data structures and operations for manipulating numerical tables and time series.
Its name is a play on the phrase "Python data analysis".
"""

from flask import Flask, request, render_template
import pandas as pd
import requests
# import webbrowser
# The webbrowser module provides a high-level interface to allow displaying Web-based documents to users.


app = Flask(__name__)
# clear the cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['POST', 'GET'])  # Flask app - Janet
def root_page():
    ingredient = ''     # user's ingredient for searching on
    max_time = ''       # user's cooking & prep time limit
    cuisine = ''        # cuisine type
    health = ''         # health label
    if request.method == 'POST' and ('userfood' and 'usertime' and 'usercuisine' and 'userhealth') in request.form:
        ingredient = request.form.get('userfood')       # ingredient
        max_time = int(request.form.get('usertime'))    # max cooking time was a string
        cuisine = request.form.get('usercuisine')       # cuisine type (e.g. Chinese, Eastern European)
        health = request.form.get('userhealth')         # health label (e.g. vegan, gluten-free)
        recipe_search(ingredient, max_time, cuisine, health)
        run_csv(ingredient, max_time, cuisine, health)
    return render_template("index.html", ingredient=ingredient, max_time=max_time, cuisine=cuisine, health=health)


@app.route('/recipes', methods=['GET', 'POST'])     # Flask renders pandas' html table
def recipes_html():
    return render_template('recipes.html')


def recipe_search(ingredient, max_time, cuisine, health):
    app_id = 'YOUR_ID'
    app_key = 'YOUR_KEY'
    # get your own id & key, free of charge, from https://developer.edamam.com/
    if health == 'none':  # for health result 'none', do not add health as a search term for API - Alex
        result = requests.get(
        'https://api.edamam.com/search?q={}&app_id={}&app_key={}&time=1-{}&cuisineType={}'.format(ingredient, app_id, app_key, max_time, cuisine))
    else:
        result = requests.get('https://api.edamam.com/search?q={}&app_id={}&app_key={}&time=1-{}&cuisineType={}&health={}'.format(ingredient, app_id, app_key, max_time, cuisine, health))
    data = result.json()
    return data['hits']


# Alex's pandas
def run_csv(ingredient, max_time, cuisine, health):
    d = []  # clear the dataset
    # ingredient = input('Enter an ingredient: ')  - Commented out by Janet
    results = recipe_search(ingredient, max_time, cuisine, health)

    if results != []:             # IF search result is not empty, create the table
        for item in results:
            recipe = item['recipe']
            label = recipe['label']
            cuisine = str(recipe['cuisineType'])  # convert to string - Alex
            allowed_chars = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ ,')
            # set allowed characters (we want to keep letters + commas) - Alex
            cuisine = ''.join(filter(allowed_chars.__contains__, cuisine))
            # extract only allowed characters, as set above - Alex

            calories = round(recipe['calories'])        # rounded to nearest integer - Janet
            carbs = round(recipe['totalNutrients']['CHOCDF']['quantity'])  # grams of carbohydrates
            fat = round(recipe['totalNutrients']['FAT']['quantity'])  # grams of fat
            protein = round(recipe['totalNutrients']['PROCNT']['quantity'])  # grams of protein

            # total time to prep and cook recipe - not foolproof as depends on original recipe listing
            time = round(recipe['totalTime'])
            link = recipe['url']
            # webbrowser.open(link)  # automatically open web browser tabs for each recipe
            # disable during development :)

            d.append(
                {
                    'Search term': ingredient,
                    'Recipe name': label,
                    'Cuisine Type': cuisine,
                    'Diet type': health,
                    'Total time': time,
                    'Calories': calories,
                    'CHO': carbs,
                    'Fat': fat,
                    'Protein': protein,
                    'URL': link,
                }
            )
        recipe_df = pd.DataFrame(d)
        recipe_df.to_csv('recipe-search.csv', index=False)
        apples_recipes = pd.read_csv('recipe-search.csv')       # Read the csv file
        apples_recipes['URL'] = '<a href=' + apples_recipes['URL'] + '><div>' + apples_recipes['URL'] + '</div></a>'
        # Set hyperlink - Alex
        apples_recipes.to_html('./templates/recipes.html', escape=False)
        # then convert to a recipes.HTML page - Janet
        # escape=False needed for hyperlink to render - Alex

    else:
        print('No search results!')
        # IF search result is empty, print a message to the console and don't run the rest of the program.
        # The recipes.html page will not be regenerated, but the user will see the previous results.
        # They can self correct, as it will difficult for us to error check on spelling;
        # spelling varies from country to country and some recipe names are misspelt anyway.


app.run()
