from flask import Flask, render_template, request,\
    redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import random
import string
import httplib2
import json
import requests
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'catalog',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

import models
from models import Base, Category, Item, User

# engine = create_engine('sqlite:///categoryapp.db')
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/catalog', pool_pre_ping=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# """
# Some code for authentication and authorization checks inspired by examples found in instructor notes. StackOverflow and the official Flask documentation were also used as guides when I got stuck, as well as the Udacity forums.
# """

# engine = create_engine('sqlite:///categoryapp.db')
# Base.metadata.bind = engine

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

@app.route('/login')
def showLogin():
    """
    Takes the user to the login page.
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Gathers data from Google Sign In API and places it inside
    a session variable.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    req = h.request(url, 'GET')[1]
    req_json = req.decode('utf8').replace("'", "'")
    result = json.loads(req_json)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already\
         connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    """
    We need to create a user here if one doesn't already exist
    in our database. This is crucial for authorization checks
    to work. This code was inspired by instructor notes.
    """
    # Use the helper function for getting the user ID
    user_id = getUserID(login_session['email'])
    if not user_id:
        # if the user doesn't exist yet, create one
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img style="width: 200px;" src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:\
     150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    """
    Deletes the user session variables and resets the session.
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
        login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("You have been successfully logged out.")
        return redirect('/catalog')
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# All categories
@app.route('/')
@app.route('/catalog')
def showCategories():
    """
    Show all categories in my catalog.
    """
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)


@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/items')
def showItems(category_id):
    """
    Show all items in a specified category.
    """
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    if 'username' not in login_session:
        return render_template('publicitems.html', items = items)
    else:
        return render_template('item.html', category=category, items=items)


@app.route('/catalog/<int:category_id>/items/new', methods=['GET', 'POST'])
def newItem(category_id):
    """
    Add a new item to a specified category.
    """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        item = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category_id,
            user_id = login_session['user_id'])
        session.add(item)
        session.commit()
        flash("New item %s created." % item.name)
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    """
    Edit the specified item in a specified category.
    """
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    user_id = login_session.get('user_id')
    if item.user_id != user_id:
        flash("You are not authorized to edit %s" % item.name)
        return redirect(url_for('showItems', category_id=category_id))
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        session.add(item)
        session.commit()
        flash("Catalog item %s updated." % item.name)
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('editItem.html', category_id=category_id,
                               item=item)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    """
    Delete a specified item within a specified category
    """
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    user_id = login_session['user_id']
    if item.user_id != user_id:
        flash("You are not authorized to delete %s" % item.name)
        return redirect(url_for('showItems', category_id=category_id))
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item %s deleted." % item.name)
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteItem.html',
                               category_id=category_id, item=item)

# JSON endpoints
@app.route('/catalog/JSON')
def catalogJSON():
    """
    JSON endpoint for showing all categories.
    """
    categories = session.query(Category).all()
    return jsonify(Categories=[r.serialize for r in categories])


@app.route('/catalog/<int:category_id>/items/JSON')
def categoryItemJSON(category_id):
    """
    JSON endpoint for showing all items in a specified category.
    """
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


if __name__ == '__main__':
    app.run()
