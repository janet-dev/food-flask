# food-flask

Python with Flask recipe search app
<br><br>
This Code First Girls: Team 'Apple' Project (April 2021) runs a programme written in Python, to search online for recipes based on an ingredient, cuisine origin and maximum time. It uses the Edamam Recipe API to get a dataset of up to ten recipe web links for the user to inspect. A table in the form of a CSV file, created by the Python library Pandas, is saved on the user's device for future reference, and then shown on the recipes.html webpage.
<br><br>
Note: the CSV file is overwritten on each run of the search and a new recipes.html is created.<br>
You will need your own id & key from  https://developer.edamam.com/
<br><br>
Features created by this Python programme are rendered here on this webpage by the Python library, Flask and via Jinaj2 templates. Pure.CSS is ridiculously tiny and used to style this page. The entire set of modules clocks in at 3.7KB minified and gzipped. Crafted with mobile devices in mind it was important to keep the file sizes small, and every line of CSS was carefully considered. Pure builds on Normalize.css and provides layout and styling for native HTML elements, plus the most common UI components. Pure is responsive out of the box, so elements look great on all screen sizes.
<br><br>
Meet Team 'Apple':<br>
Aleksandra Kulawska<br>
Angela Chan<br>
Janet Dornan
<br><br>
A huge thank you to our wonderful, supporting, inspiring instructors:<br>
Deanna Green<br>
Rabia Mahmood<br>
Ellen Wootten
<br><br>
and also to David Clode for his photograph of a rare green tree python.<br>
<br><br>
Users are asked to enter 4 choices:<br>
- an ingredient: limited to one word of <20 letters<br>
- cuisine origin: this is a drop down list with the first item as the default<br>
- dietary requirements: drop down list with a default of 'none'<br>
- max time for preparing + cooking the recipe: limited to a positive number
<br><br>
If, for some reason the user types in rubbish for the ingredient, an empty result will be returned from Edamam.<br>
The program checks for an empty search result and prints an advisory message to the PyCharm console.<br>
The recipes.html will not be regenerated and the user will see the previous results or no page.<br><br>
This program uses the Edamam API Version 1<br>
https://developer.edamam.com/edamam-docs-recipe-api-v1<br>


