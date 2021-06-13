# Ticket Management System -Python -Flask
An event ticket management system using Python, Flask and Jinja2


## Technical Choices
### Libraries
[Flask 2.0.1](https://flask.palletsprojects.com/en/2.0.x/), [Flask-SQLAlchemy 2.5.1](https://flask-sqlalchemy.palletsprojects.com/en/2.x/), [SQLAlchemy 1.4.17](https://www.sqlalchemy.org/), [Jinja2 3.0.1](https://jinja.palletsprojects.com/en/3.0.x/)

## File to run:
app.py located in the root directory in this repo.


## Live Demonstration
For clarity I have decided to demonstrate the workings of the app using the animated clip embedded below.

![](/demo/webservicedemo.gif)


## GET request APIs
APIs can be tested directly from the web browser URL address bar and the changes can be verified using the frontend webservice.
<br />
/api/addticket/"name"
<br />
/redeem/"id"

## If I had more time
Design and create automated unit test to test each method.
  <br />
Explore use of database management directly rather than SQLAlchemy.
<br />
Dockerize the app: I was able to dockerise the application but was not able to test or push the image to docker-repo
