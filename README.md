# Pinecone Demo - Customer Service Chat Bot

This app is built using Python 3.9+, Flask 2.0+, and Pinecone.

You can find it [hosted on Heroku here](https://pinecone-demo.herokuapp.com/).

## Running the app locally

Begin by cloning this git repo and navigating to the project directory.

Next, create a virtual environment and activate it:

```
python -m venv venv
. venv/bin/activate
```

Install dependencies by running:

```
python -m pip install -r requirements.txt
```

Finally, to run the app on your machine, simply run this command from the terminal:

```
flask run
```

To run the app in debug mode, add the `FLASK_ENV=development` environment variable before the command:

```
FLASK_ENV=development flask run
```

The app should now be running on http://127.0.0.1:5000 in your browser.

## Deploying the app to Heroku

You can deploy this app to Heroku using the following steps:

1. `heroku login` (Logs in to the Heroku CLI)
2. `heroku create pinecone-demo` (You will need to use a unique name)
3. `git push heroku master` (Pushes your latest code)
4. `heroku open` (Opens the hosted app in your browser)

## Resources

Python, pyenv, and pip
- https://realpython.com/intro-to-pyenv/
- https://github.com/pyenv/pyenv
- https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-shell
- https://pip.pypa.io/en/latest/user_guide/#requirements-files
- https://www.twilio.com/blog/environment-variables-python

Flask
- https://flask.palletsprojects.com/en/2.0.x/installation/
- https://flask.palletsprojects.com/en/2.0.x/quickstart/
- https://flask.palletsprojects.com/en/2.0.x/tutorial/
- https://github.com/pallets/flask/tree/main/examples/tutorial
- https://flask.palletsprojects.com/en/2.0.x/api/#flask.Request

Heroku and Python
- https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true
- https://realpython.com/flask-by-example-part-1-project-setup/

Pinecone
- https://www.pinecone.io/docs/quickstart-python/
- https://www.pinecone.io/docs/examples/question-answering/
- https://docs.beta.pinecone.io/en/latest/python_client/manage.html
