WASPGpt is a Web Application Security Project that I am developing and testing to determine how well the ChatGpt API can be utilized against a wide range of attacks.
I will automate everything in this application to minimize user input. You will only need an authentication key from OpenAI to use the ChatGPT API.
This key will be looked for in the .env file, if it is not found the application will prompt you to enter the key.

# Database:
This database uses sqlite3, database is stored outside the project folder, in the instance folder.

# Websites and resources used for this project:
https://flask.palletsprojects.com/en/3.0.x/
https://openai.com/


# Running the Application

First you need to navigate to the folder your Application is installed in.
Next you'll need to initialize the database. Run this command to do so: flask --app WASPGpt init-db
Then to run this application, run this command: flask --app WASPGpt run --debug
(The debug tag is for testing purposes, gives you access to the console to see what's going on, or wrong.)

By default, flask uses port 5000. You can specify a certain port to use e.g. flask run --port {port}