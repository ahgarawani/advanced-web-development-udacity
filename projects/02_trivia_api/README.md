# Full Stack Trivia API
Hello and welcome to to my version of the Full Stack Trivia API, the final project to Udacity's Full Stack Web Development Nanodegree. I hope you have a great time.
## Introduction

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where I came in! I Helped them finish the trivia app by building the API. The application now has the functionality to:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

### Project Structure
First things first, let's take a look at the structure of the project folder.

#### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server.

  ```sh
  ├── README.md
  ├── backend 
  |   ├── flaskr 
  |   |   └── __init.py__ *** this is where the endpoint handlers live.
  │   ├── models.py *** this is where the models of the database live.
  │   ├── requirements.txt *** this is where the python dependencies neccessary for this project live.
  │   ├── test_flaskr.py *** this is where the unittest functions live.
  │   └── trivia.psql *** this is a sequence of sql commands that will populate the database.
  |
  └── frontend 
  ```
  
#### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. What would matter to you in this folder is `./frontend/src/components` and its contents.
  ```sh
  ├── README.md
  ├── backend 
  |
  └── frontend
      ├── package.json
      ├── package-lock.json
      ├── public 
      └── src
          ├── App.js
          ├── App.test.js
          ├── index.js
          ├── logo.svg
          ├── serviceWorker.js
          ├── components 
          |   ├── Header.js *** this script renders a the navigation bar.
          |   ├── FormView.js *** this script renders question creation webpage .
          |   ├── Question.js *** this script renders a webpage with a single question.
          |   ├── QuestionView.js *** this script renders a webpage with a a paginated list of questions.
          |   ├── QuizView.js *** this script renders a the quiz webpage.
          |   └── Search.js *** this script renders the search webpage.
          └── stylesheets
  ```

### Installation

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

It's recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.org/en/download/package-manager/](https://nodejs.org/en/download/package-manager/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### PostgreSQL 12

PostgreSQL is an open-source relational database management system that is popular for web development. To install the latest version of PostgreSQL for your platform follow the instructions in the [PostgreSQL docs](https://www.postgresql.org/download/).

### Database Setup
First, you have to make sure the posgresql server is running.

With Postgresql server running, create a database called 'trivia' by running in terminal:
```bash
createdb trivia
```
Then, populate the database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Quick Start

Let's try and run our app.

### Running the backend server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

### Running the frontend server in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file.

From within the `frontend` directory run:

```bash
npm start
```

That should have started the server. Now, open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

### Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```

## API

Now, onto what are the endpoints in the app and what each one does.

### Endpoints

- GET `/categories`
- GET `/questions?page=<page_number>` 
- POST `/questions`
- POST `/questions/search`
- DELETE `/questions/<int:question_id>`
- GET `/categories/<int:category_id>/questions`
- POST `/quizzes`


#### GET `/categories`
- Fetches a dictionary of all available categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None.
- Returns: An object with two keys, success, that equals True and categories, that contains an object of id: category_string key:value pairs.
- Sample response: 
  ```bash
  {
    "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "success": true
  }
  ```

#### GET `/questions?page=<page_number>`
- Fetches a paginated dictionary of 10 questions per page from all available categories in which the keys are object value pairs.
- Request Arguments (Optional): page_number (int)
- Returns: An object with five keys:
  - categories: a dictionary of all categories formatted as an object of id: category_string key:value pairs.
  - current_category: `null` because no specific category is selected.
  - questions: a list of paginated questions, each element is dictionary of on one question.
  - success: `True`.
  - total_questions: the total number of all questions in the entire database.
- Sample response: 
  ```bash
  {
    "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "current_category": null, 
    "questions": [
      {
        "answer": "Apollo 13", 
        "category": 5, 
        "difficulty": 4, 
        "id": 2, 
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      }, 
      {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      }, 
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Muhammad Ali", 
        "category": 4, 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
      }, 
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }, 
      {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
      }, 
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }
    ], 
    "success": true, 
    "total_questions": 19
  }
  ```
- Aborts with a `404` if the `page_number` is too high to contain any questions in it.

#### POST `/questions`
- Adds a question to the database.
- Request Arguments: {question:string, answer:string, difficulty:int, category:string}
- Returns: An object with three keys:
  - created: the id of the newly created questions.
  - success: `True`.
  - total_questions: the total number of all questions in the entire database.
- Sample response: 
  ```bash
  {
    "created": 24, 
    "success": true, 
    "total_questions": 20
  }
  ```

#### POST `/questions/search`
- Adds a question to the database.
- Request Arguments: {searchTerm:string}
- Returns: An object with four keys:
  - current_category: should be `null`.
  - questions: a list of the search results.
  - success: True.
  - total_questions: the number of the search results.
- Sample response: 
  ```bash
  {
    "current_category": null, 
    "questions": [
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }
    ], 
    "success": true, 
    "total_questions": 1
  }
  ```

#### DELETE `/questions/<int:question_id>`
- Deletes a question from the database.
- Request Arguments: question_id (int), that is the id of the question to be deleted. 
- Returns: An object with six keys:
  - categories: a dictionary of all categories formatted as an object of id: category_string key:value pairs.
  - current_category: `null` because no specific category is selected.
  - deleted: the id of the deleted question.
  - questions: a list of paginated questions, each element is dictionary of on one question.
  - success: `True`.
  - total_questions: the total number of all questions in the entire database.
- Sample response: 
  ```bash
  {
    "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "current_category": null, 
    "deleted": 32, 
    "questions": [
      {
        "answer": "Apollo 13", 
        "category": 5, 
        "difficulty": 4, 
        "id": 2, 
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      }, 
      {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      }, 
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Muhammad Ali", 
        "category": 4, 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
      }, 
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }, 
      {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
      }, 
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }
    ], 
    "success": true, 
    "total_questions": 19
  }
  ```

#### GET `/categories/<int:category_id>/questions`
- Fetches a list of all questions in a given category.
- Request Arguments: category_id (int), that is the id of the category in which the questions will be retrieved.
- Returns: An object with five keys:
  - categories: a dictionary of all categories formatted as an object of id: category_string key:value pairs.
  - current_category: the id of the category *category_id*.
  - questions: a list of all questions in the given category.
  - success: True.
  - total_questions: the total number of questions in the given category.
- Sample response: 
  ```bash
  {
    "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "current_category": 6, 
    "questions": [
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }
    ], 
    "success": true, 
    "total_questions": 2
  }
  ```

#### POST `/quizzes`
- Fetches a list of previously undisplayed questions in a given category.
- Request Arguments: {previous_questions: [], quiz_category: {type: "Art", id: "2"}}
- Returns: An object with five keys:
  - question: a dictionary containing a randomly chosen question from the given category.
  - success: True.
- Sample response: 
  ```bash
  {
    "question": {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    "success": true
  }
  ```