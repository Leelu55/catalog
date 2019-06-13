
# Udacity Full Stack Web Developer Nanodegree Project: Linux Server Configuration

[Full Stack Web Developer Nanodegree](https://eu.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

- The **catalog**(https://github.com/Leelu55/catalog) web app written in Python, HTML, CSS and Javascript provides lists of books within book categories like fiction or poetry.

-**catalog**is deployed to a [Amazon Lightsail](https://lightsail.aws.amazon.com/) Linux server instance with Ubuntu 18.04 OS, [Apache2](https://httpd.apache.org/) Web Server and [PostgreSQL](https://www.postgresql.org/) relational database

-The web application Collective Library can be accessed at [http://www.amberjack.org](http://www.amberjack.org)

-The server's IP Adress is **3.121.185.101** and the SSH Port is 2200. It is only accessible via key-based SSH authentication. The key to the grader will be provided as stated

## Installed software

- **SQLAlchemy Toolkit and ORM**

[Download and Installation Instructions](https://docs.sqlalchemy.org/en/13/intro.html)
```
pip install SQLAlchemy
```

- **Flask Python web framework**

[Download and Installation Instructions](http://flask.pocoo.org/docs/1.0/installation/#installation)
```
  pip install flask
```

- **Materialize CSS**
[Download and Installation Instructions](https://materializecss.com/getting-started.html)


- **Google OAuth 2.0 for Server-side Web Apps**
```
 pip install --upgrade google-api-python-client
```

- **install PostgreSQL and create db**
```
sudo apt install postgresql postgresql-contrib
```

```
sudo -u postgres createdb catalog
```
The user for the postgresql (catalog) db catalog as well as the password (written into /etc/environment) were set  using

```
sudo -i -u postgres
```

```
postgres=# ALTER USER catalog WITH ENCRYPTED PASSWORD '<PASSWORD>'
```

also for use of PostgreSQL and Python installed **psycopg2**

```
sudo -H pip install psycopg2
```

-**Install git and commit catalog project**

for testing and modifying git was installed, a git repo inside the /var/www/catalog directory initialized and used for version controll
```
sudo apt-get install git
```
inside /var/www/catalog
```
sudo git init
```

-**Installed python mod_wsgi package for Python 2**

The mod_wsgi module for Apache2 for enabling the execution of python scripts by the web server
```
sudo apt-get install libapache2-mod-wsgi
```

also activated the module

```
sudo a2enmod wsgi
```

## Config changes

1. **Create new user grader**
2. **Add grader to sudoers**
3. **Disable Root Login**
4. **Enable SSH key authorization**
5. **Enforce SSH key-based only remote login**
6. **Add ports to Ubuntu Firewall and enable Firewall**
7. **Add ports in Lightsail instance**
8. **add SSH port on non default host**


## Built With

* [SQLAlchemy](https://www.sqlalchemy.org/) - Toolkit and ORM
* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework used
* [Materialize](https://materializecss.com/) - CSS Framework
* [Google APIs Client Library for Python](https://developers.google.com/api-client-library/python/) - OAuth Provider

## Authors

* **[[Maria]](https://github.com/Leelu55/)**

See also the list of [contributors](https://github.com/Leelu55/catalog/contributors) who participated in this project.

## Acknowledgments

* Inspirations : Full Stack Web Developer Nanodegree code


