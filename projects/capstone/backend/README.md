# Casting Agency 
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.Authorised users will be able to create, view, update, delete movies and actors details.

Backend url : https://shrinivas-capstone.herokuapp.com/

### Installing Dependencies for the Backend

1. **Python 3.8** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


### Running the server

To run the server, execute:

```bash
python3 app.py
```


## API Endpoints

GET  '/movies'
- Returns all the movies
- Roles authorized : Casting Assistant,Casting Director,Executive Producer. 

Sample response: 

```json
{
    "movies": [
        {
            "id": 6,
            "release_date": "Wed, 27 Apr 2022 18:30:00 GMT",
            "title": "Top Gun: Maverick1"
        }
    ],
    "success": true
}

```
GET /movies/<int:id>
- Fetches movies based on the specific id provided 
- Request Arguments: page:int
- Roles authorized : Casting Assistant,Casting Director,Executive Producer.

sample response: 

```json
{
 "movie": {
        "id": 6,
        "release_date": "Wed, 27 Apr 2022 18:30:00 GMT",
        "title": "Top Gun: Maverick"
    },
    "success": true
}

```

POST /movies
- Creates a new movie based on a payload.
- Request Body: {'title': 'Jurassic','release_date': '28/04/2022'} (all fields are mandatory)
- Roles authorized : Executive Producer.

sample response: 

```json

{
 "movie": {
    "id": 3,
    "release_date": "Wed, 27 Apr 2022 18:30:00 GMT",
    "title": "Top Gun: Maverick"
  },
  "success": true
}
```

PATCH /movies/<int:id>
- Updates a movies based on payload.
- Roles authorized : Casting Director, Executive Producer.

sample response: 

```json

{
 "movie": {
    "id": 3,
    "release_date": "Wed, 27 Apr 2022 18:30:00 GMT",
    "title": "Top Gun: Maverick updated"
  },
  "success": true
}
```

DELETE /movies/int:id
- Deletes a movie based on url query parameter
- Roles authorised: Executive Producer.

sample response: 

```json
{
 "message": "movie id 6, titled Top Gun: Maverick is deleted",
 "success": true
}
```

GET /actors
- Returns all the actors
- Roles authorized : Casting Assistant,Casting Director,Executive Producer.

sample response: 

```json
{
"actors": [
    {
      "age": 40,
      "gender": "male",
      "id": 1,
      "name": "Will Smith"
    },
    {
      "age": 50,
      "gender": "male",
      "id": 2,
      "name": "Sam Neill"
    }
  ],
  "success": true
  }
```

GET /actors/<int:id>
- Fetches actor based on the id provided
- Roles authorized : Casting Assistant,Casting Director,Executive Producer.

sample response: 

```json
{
  "actor": {
    "age": 40,
    "gender": "male",
    "id": 1,
    "name": "Will Smith"
  },
  "success": true
}
```

POST /actors
- Creates new actor based on the payload provided
- Roles authorized : Casting Director,Executive Producer.

sample response: 

```json
{
  "actor": {
    "age": 22,
    "gender": "female",
    "id": 3,
    "name": "Bryce Dallas"
  },
  "success": true
}
```

PATCH /actors/<int:id>
- Updates an actor details based on the payload provided
- Roles authorized : Casting Director,Executive Producer.

sample response: 

```json
{
  "actor": {
    "age": 32,
    "gender": "female",
    "id": 3,
    "name": "Laura Dern"
  },
  "success": true
}
```

DELETE /actors/int:id
- Deletes an actor based on id provided in url query parameter
- Roles authorized : Casting Director,Executive Producer.

sample response: 

```json
{
  "message": "actor id 3, named Laura Dern is deleted",
  "success": true
}

```


## Error Responses
400 – bad request
401 – unauthorized
404 – resource not found
422 – unprocessable
500 – internal server error

Sample error response

```json
{
 "error": 422,
 "success": false
 "message": "Not processable"
}
```

Sample RBAC error response

```json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
```

## Testing
To run the tests,

Replace the jwt tokens in test_app.py with the ones generated on the website.

For testing locally, we need to reset database. To reset database, run
```
python manage.py db downgrade
python manage.py db upgrade

```

```
python3 test_app.py
```
