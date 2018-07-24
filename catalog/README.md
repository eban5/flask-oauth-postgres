# Catalog App (FSND Part 3)

The Catalog App is an example RESTful CRUD web application built with the Flask framework, Boostrap v4, and using the Google Sign-in Third Party Authentication mechanism.

## How to run the project

You'll need to configure a few things before you can successfully run this project.

1. Install Vagrant and Virtualbox onto your machine
2. Clone this repository
3. Change directories `cd` to the cloned repository directory
4. Launch the Vagrant VM with `vagrant up`
5. Install dependencies with `sudo pip install werkzeug==0.8.3, flask==0.9, Flask-Login==0.1.3`
6. Run the database setup script with `python database_setup.py`, which will populate the database with demo data
7. Build the data model by running `python models.py`
8. Run the application with `python application.py`

The application will now be running on http://localhost:8000

