# Project Proposal

Use this template to help get you started right away! Once the proposal is complete, please let your mentor know that this is ready to be reviewed.

## Get Started

|            | Description                                                                                                                                                                                                                                                                                                                                              | Fill in |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| Tech Stack | What tech stack will you use for your final project? It is recommended to use the following technologies in this project: Python/Flask, PostgreSQL, SQLAlchemy, Heroku, Jinja, RESTful APIs, JavaScript, HTML, CSS. Depending on your idea, you might end up using WTForms and other technologies discussed in the course.                               |         |
| Type       | Will this be a website? A mobile app? Something else?                                                                                                                                                                                                                                                                                                    |         |
| Goal       | What goal will your project be designed to achieve?                                                                                                                                                                                                                                                                                                      |         |
| Users      | What kind of users will visit your app? In other words, what is the demographic of your users?                                                                                                                                                                                                                                                           |         |
| Data       | What data do you plan on using? How are you planning on collecting your data? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain. You are welcome to create your own API and populate it with data. If you are using a Python/Flask stack, you are required to create your own API. |         |

# Breaking down your project

When planning your project, break down your project into smaller tasks, knowing that you may not know everything in advance and that these details might change later. Some common tasks might include:

- Determining the database schema
- Sourcing your data
- Determining user flow(s)
- Setting up the backend and database
- Setting up the frontend
- What functionality will your app include?
  - User login and sign up
  - Uploading a user profile picture

Here are a few examples to get you started with. During the proposal stage, you just need to create the tasks. Description and details can be edited at a later time. In addition, more tasks can be added in at a later time.

| Task Name                   | Description                                                                                                   | Example                                                           |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Design Database schema      | Determine the models and database schema required for your project.                                           | [Link](https://github.com/hatchways/sb-capstone-example/issues/1) |
| Source Your Data            | Determine where your data will come from. You may choose to use an existing API or create your own.           | [Link](https://github.com/hatchways/sb-capstone-example/issues/2) |
| User Flows                  | Determine user flow(s) - think about what you want a user’s experience to be like as they navigate your site. | [Link](https://github.com/hatchways/sb-capstone-example/issues/3) |
| Set up backend and database | Configure the environmental variables on your framework of choice for development and set up database.        | [Link](https://github.com/hatchways/sb-capstone-example/issues/4) |
| Set up frontend             | Set up frontend framework of choice and link it to the backend with a simple API call for example.            | [Link](https://github.com/hatchways/sb-capstone-example/issues/5) |
| User Authentication         | Fullstack feature - ability to authenticate (login and sign up) as a user                                     | [Link](https://github.com/hatchways/sb-capstone-example/issues/6) |

## Labeling

Labeling is a great way to separate out your tasks and to track progress. Here’s an [example](https://github.com/hatchways/sb-capstone-example/issues) of a list of issues that have labels associated.

| Label Type    | Description                                                                                                                                                                                                                                                                                                                     | Example                      |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Difficulty    | Estimating the difficulty level will be helpful to determine if the project is unique and ready to be showcased as part of your portfolio - having a mix of task difficultlies will be essential.                                                                                                                               | Easy, Medium, Hard           |
| Type          | If a frontend/backend task is large at scale (for example: more than 100 additional lines or changes), it might be a good idea to separate these tasks out into their own individual task. If a feature is smaller at scale (not more than 10 files changed), labeling it as fullstack would be suitable to review all at once. | Frontend, Backend, Fullstack |
| Stretch Goals | You can also label certain tasks as stretch goals - as a nice to have, but not mandatory for completing this project.                                                                                                                                                                                                           | Must Have, Stretch Goal      |

Project Description: Recipe Discovery Website

Overview:
The website aims to provide users with a solution to the common question, "What can I make with these ingredients?". Users can input their available ingredients using the 'spoonacular' API, and the platform will generate recipes that utilize those ingredients. The website will also suggest recipes that require only a few additional ingredients to complete the dish.

Key Features:

Ingredient-Based Search:

Users input their available ingredients.
'spoonacular' API fetches recipes that exclusively use entered ingredients and require minimal additional items.
"My Menu" Tab:

Users can pin favorite recipes to a personalized "My Menu" tab.
Convenient access to saved recipes for future use.

Stretch Goals (Time-Dependent):
Some of these features may be included in the final product, depending on time availability.

Recipe Substitutions:

Explore the addition of ingredient substitutions for broader search parameters.

Rating System:
Users can provide ratings on a 0-5 star scale across multiple categories, such as complexity, time, and taste. They can also include notes like “Could use more salt.” These detailed ratings will be appended to each recipe, allowing other users to make informed decisions.

User-Generated Content:

Encourage users to contribute their recipes, expanding the platform's database.

-Set up backend and database | Configure the environmental variables on your framework of choice for development and set up a database.

TODO:

-To set up a NodeJS/Express server
-setup SQLite database

Fullstack feature - ability to authenticate (login and sign up) as a user

Ability to log in and sign up as a user

Users will be able to log in and sign up on the front end by entering email and password.
The user will be authenticated and logged in if successfully logged in or signed up.

Make a similar paragraph like the one below using https://spoonacular.com/food-api/
Using this API, I will utilize:
-Recipes
-Ingredients
-Diet restrictions

Technology Stack:
The program will leverage a robust technology stack to ensure efficient functionality and a seamless user experience.

Backend (Python/Flask):

Utilizes Python with the Flask web framework for the backend.
Implements Flask-SQLAlchemy to interact with the PostgreSQL relational database, following the provided schema.
Database (PostgreSQL):

Employs PostgreSQL as the relational database to store user data, recipes, and ratings.
Adheres to the designed schema to maintain data integrity and relationships.
ORM (SQLAlchemy):

Utilizes SQLAlchemy as the Object-Relational Mapping (ORM) tool to facilitate interaction between the Python application and the relational database.
API Integration (Spoonacular API):

Implements the 'spoonacular' API to enhance the platform's recipe suggestions.
Utilizes RESTful APIs for seamless communication between the backend and the 'spoonacular' API.
Frontend (JavaScript, HTML, Jinja, WTForms):

Develops an intuitive and user-friendly frontend using JavaScript for dynamic interactions.
Utilizes HTML for structuring web pages, Jinja for template rendering, and WTForms for form handling.

ORDER OF PROCESS:
Setting up necessary servers and installation of any tools necessary.
Creating forms for users to input ingredients.
Get core working of API. Pulling up recipes and their ingredients based on entered search parameters. Changes to those parameters based on entered diet restrictions. Pulling up a set amount based on ingredients provided and allowing users to see different results by clicking “Other options.”
Creating separate pages to display recipes for easier readability, including more details.
Create a ‘My menu’ page where users can choose recipes they’d like to save.
Creating Users so they can log in in and be able to access and edit the “My Menu Page.”
Adding CSS and working on User Flow so that the website is easier to navigate through.
