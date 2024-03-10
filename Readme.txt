WASPGpt is a Web Application Security Project that I am developing, it utilizes HTML, and CSS for the front end, with Flask, and Sqlite3 for the backend.
The only thing that is required of you is to buy an authentication key from OpenAI to use the ChatGPT API.
This key will be looked for in a file, if it is not found the application will first prompt you to enter the key.

# Database:
This database uses sqlite3, database is stored outside the project folder, in the instance folder.

# Websites and resources used for this project:
https://flask.palletsprojects.com/en/3.0.x/
https://openai.com/


# Running the Application

First you need to navigate to the folder your Application is installed in.
Next you'll need to initialize the database. Run this command to do so: flask --app WASPGpt init-db
Then you'll need to fill the database with data, you can do this by running this command: flask --app WASPGpt fill-db (This checks the for the json file, which contains data in the Project directory.)
Then to run this application, run this command: flask --app WASPGpt run --debug
(The debug tag is for testing purposes, gives you access to the console to see what's going on, or wrong.)

By default, flask uses port 5000. You can specify a certain port to use e.g. flask run --port {port}

