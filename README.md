# flask-oauth-postgres

## FSND Part 5

The Catalog App is an example RESTful CRUD web application built with the Flask framework, Boostrap v4, and using the Google Sign-in Third Party Authentication mechanism.

```
IP Address: 52.14.20.77
SSH Port: 2200
Complete Web App URL: http://52.14.20.77.xip.io/
```

A few of the libraries used in this project were Flask, SQL-Alchemy, psycopg2 (to talk to Postgres), and PostgresSQL. The web server was configured to use a WSGI file to make the Flask app accessible by Apache (our web server software). Apache was configured to point at that WSGI file to then server requests/responses to our web application. 

The blog post found here was very useful in helping me understand what it would take to replace SQLite with a full-blown Postgres database. https://blog.theodo.fr/2017/03/developping-a-flask-web-app-with-a-postresql-database-making-all-the-possible-errors/

### Clone the repository

Additionally, rename the resulting directory to something simple like "catalog" as it is in the below examples:

```
cd /var/www/
git clone https://github.com/eban5/flask-oauth-postgres
mv flask-oauth-postgres/ catalog/
```

### Install
Install the following libraries to get the basic dependencies on your server:

```
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install apache2 postgresql postgresql-contrib libpq-dev git libapache2-mod-wsgi
```

### Create a new database
Create a new database called "catalog" and grant a new user, named "catalog", full access to this database. 

### Firewall Settings
Execute the following to set your Ubuntu firewall (ufw) properly:

``` 
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2200/tcp www 123/tcp
sudo ufw enable
```

### Setup Apache
Create an Apache conf file to hold our site's settings.

```
sudo vim /etc/apache2/sites-available/Catalog.conf
```

And use similar settings as below:

```
<VirtualHost *:80>
  ServerName 52.14.20.77.xip.io
  WSGIScriptAlias / /var/www/catalog/wsgi.py

  <Directory /var/www/catalog>
          Order allow,deny
          Allow from all
  </Directory>

  ErrorLog ${APACHE_LOG_DIR}/error.log
  LogLevel warn
  CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

```

Then enable the new site and reload Apache.

```
sudo a2ensite Catalog.conf
sudo service apache2 reload
```

### Install Python Dependencies

```
cd /var/www/catalog/
pip install -r requirements.txt
```

Also, generate a JSON file with your Google OAuth client secrets and place it in `/var/www/catalog/`.
