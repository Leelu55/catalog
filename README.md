
# Udacity Full Stack Web Developer Nanodegree Project: Linux Server Configuration

[Full Stack Web Developer Nanodegree](https://eu.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

- The **catalog**(https://github.com/Leelu55/catalog) web app written in Python, HTML, CSS and Javascript provides lists of books within book categories like fiction or poetry.

- **catalog**is deployed to a [Amazon Lightsail](https://lightsail.aws.amazon.com/) Linux server instance with Ubuntu 18.04 OS, [Apache2](https://httpd.apache.org/) Web Server and [PostgreSQL](https://www.postgresql.org/) relational database

- The web application Collective Library can be accessed at **[http://www.amberjack.org](http://www.amberjack.org)**

- The server's IP Adress is **18.196.26.71** and the SSH Port is 2200. It is only accessible via key-based SSH authentication. The key to the grader will be provided as stated

## Server login for grader
```
ssh grader@18.196.26.71 -p 2200 -i ~/PATH/TO/SAVED/PRIVATE/KEY
```

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

- **Installed PostgreSQL and create db**
```
sudo apt install postgresql postgresql-contrib
```

```
sudo -u postgres createdb catalog
```
- user for the postgresql (catalog) db catalog as well as the password (written into /etc/environment) were set using

```
sudo -i -u postgres
```

```
postgres=# ALTER USER catalog WITH ENCRYPTED PASSWORD '<PASSWORD>'
```
- also for use of PostgreSQL and Python installed **psycopg2**

```
sudo -H pip install psycopg2
```

- **Installed git and commit catalog project**

- for testing and modifying git was installed, a git repo inside the /var/www/catalog directory initialized and used for version controll
```
sudo apt-get install git
```
- inside ```/var/www/catalog```

```
sudo git init
```

- **Installed python ```mod_wsgi``` package for Python 2**

- The mod_wsgi module for Apache2 for enabling the execution of python scripts by the web server
```
sudo apt-get install libapache2-mod-wsgi
```

- also activated the module

```
sudo a2enmod wsgi
```

**Installed finger: user information lookup program**
```
sudo apt-get install finger
```
## Config changes

1. **Created new user grader**
```
sudo adduser grader
```
2. **Added grader to sudoers**
```
cp sudoers.d/90-cloud-init-users sudoers.d/grader
```
- in sudoers.d/grader give grader sudo rights:
```
# User rules for grader
grader ALL=(ALL) NOPASSWD:ALL
```

3. **Disabled remote Root Login editing the /etc/ssh/sshd_config file**

- Prevented ssh root login editing "PermitRootLogin" by uncommenting it and changing to:
```
PermitRootLogin no
```
4. **Added SSH port on non default host**
- Editing in the the ```/etc/ssh/sshd_config``` port by uncommenting and changing to:
```
Port 2200
```

5. **Enabled grader (and ubuntuſ) for SSH key authorization**
- On the local machine create public/private keypairs for grader
```
ssh-keygen -t rsa

Generating public/private rsa key pair.
Enter file in which to save the key (/home/leelu/.ssh/id_rsa): grader

cat grader.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9xmJEymzqNeBhgdEXRNLa3HB4qXALzMvnfiqLsHumDkuH5JayQWV6RlMC1P1BXUSNOE7Ar292b6Y4YK3zLq3ddz38WC0n8a2HKc8ztU+Rfuwkeru9g4ToiG+Ts5J7eluHgMZZOBhQ+YraVlYGujs26jKsiaXZOBvgFy3jWBjXv0ked4piul3ZN2G2WTmA1LXxDgDxxqGdeEp4qnqV06PJ7vj6VgCFsGiCsK7bJUOl74PxRhGIW1iJo5Jp39yB7+KPQJ4sR2QKvlypifNtnzho0845eahohooNpGznAfNhvGPJjJ87ToOUqj+ADLMR35vR7/33ZQ/fAgC8TWuaG7N1 leelu@leelu-XPS-13-9360
```
- Copy the public key string
- On the server as sudo user (ubuntu) in the .ssh directory created the authorized keys file
```
sudo nano authorized_keys
```
- copy the ```grader.pub```content into the```authorized_keys file```
- change permissions on  ```.ssh```directory to 700 (owner can read/write/execute) ```chmod 700 .ssh```
- change permissions on ```authorized_keys``` file to 644 (owner can read/write, read for group and everyone) ```sudo chmod 700 ~/.ssh/authorized_keys```

6. **Enforced SSH key-based only remote login**
- Editing in the the ```/etc/ssh/sshd_config``` PasswordAuthentication by uncommenting and changing to:
```
PasswordAuthentication no
```
-Then restart ssh``` sudo service ssh restart```

7. **Added ports to Ubuntu Firewall and enable Firewall**

- Check current firewall status
```sudo ufw status```

- Disable all incoming traffic
```sudo ufw default deny incoming```

- Enable all outgoing traffic
```sudo ufw default allow outgoing```

- allow ssh, www and ntp
``` sudo ufw allow ntp```
``` sudo ufw allow www```
``` sudo ufw allow ssh```

- Check current firewall status
```sudo ufw status```

- Enable firewall
```sudo ufw enable```

- also added ports in Lightsail instance in web dashboard

### Running the Application

1. Changes in catalog project files

- renamed ```views.py``` to ```catalog.py```
- create database using PostgreSQL instead of SQLite and using database password from environment variable

OLD CODE:
```
engine = create_engine('sqlite:///library.db')
```
NEW CODE:
```
engine = create_engine('postgresql://catalog:library2019@localhost:5432/catalog')
```

- in catalog.py in the code execution block at the end remove all localhost related code

OLD CODE:
```
if __name__ == '__main__':
    # setting an environment variable to test the app locally without https
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    #  set a secret key to use flask sessions
    app.secret_key = os.urandom(24)
    app.debug = True
    # run the app on http://localhost:8000
    app.run(host='0.0.0.0', port=8000)

```
NEW CODE:

```
if __name__ == '__main__':
    os.environ['DEBUG'] = '1'
    app.run()

```
2. Populating the catalog db with initial data

- Run the ```lotsof_books_categories.py``` inside the ```catalog``` directory **once**
```python lotsof_books_categories.py```

3. creating the catalog.wsgi file and configuring apache VirtualHost container
- In ```/var/www``` created the ```catalog.wsgi``` file for enabling apache2 to run the catalog application
```
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog")

from catalog import app as application
application.secret_key = 'RANDOM SECRET KEY'
```
- In ```/etc/apache2/sites-available``` edit the ```000-default.conf``` file to add the WSGIScript Alias for Apache to find the ```catalog.wsgi``` file
```
<VirtualHost *:80>
...
.
.
.
WSGIScriptAlias / /var/www/catalog.wsgi
</VirtualHost *:80>
```
- In ```/etc/apache2/sites-enabled``` edit the ``` catalog.conf``` file to provide correct IP adress, URL, alias, document root and static location

```
<VirtualHost 18.196.26.71>
                ServerName www.amberjack.org
                ServerAlias amberjack.org
                DocumentRoot /var/www/catalog
                <Directory /var/www/catalog/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/catalog/static
                <Directory /var/www/catalog/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                WSGIScriptAlias / /var/www/catalog.wsgi
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

## TODO

- To make the Google OAuth2 login work, HTTPS should be enabled, this couldn't be achieved yet.

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
