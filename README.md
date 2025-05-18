Djangology CfMS version 2
=========================

**Djangology Crowdfunding Management System** (Djangology CfMS) is a Content Management System wrote in [Django Framework](https://www.djangoproject.com/) (based on [Python](https://en.wikipedia.org/wiki/Python_%28programming_language%29)) designed for allow organizations to build themselves microcrowdfundings sites.

Djangology CfMS is a fork of [FreedomSponsors](https://github.com/freedomsponsors/www.freedomsponsors.org). Djangology CfMS is written specially for support [Funding.Wiki](https://funding.wiki) adding features related to non-software projects.

*This version is based on Django 5 / Python 3, upgrading the previous version Django 1 / Python 2.*

# Installation instructions
Clone the project

*Extra instructions in* `doc/setup.md`

`git clone https://gitlab.com/wikifunding/djangology-cfms-2 && cd djangology-cfms-2`

## 1. Install dependencies 

### 1.1 Debian
```bash
sudo apt install postgresql postgresql-contrib \
python-dev python-lxml libxslt-dev libpq-dev python-pip \
libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev \
liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk \
libxmlsec1-dev redis-server python3-venv
```
### 1.2 Ubuntu
```bash
sudo apt install postgresql-server-dev-9.6 postgresql-9.6 \
python-dev python-lxml libxslt-dev libpq-dev pgadmin3 \
libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev \
liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk \
python-pip redis-server python3-venv
```
(@Acromantula: possibly `libxmlsec1-dev` needed, too - I was propted while trying to install `dm.xmlsec.binding==1.3.2` in requirements.txt)
    
## 2. Create database:
```bash
sudo su postgres #run the next command as postgres
createuser -d -SRP djangology # this will prompt you to create a password (just use djangology for now)
createdb -O djangology djangology
psql
\c djangology
CREATE EXTENSION postgis; # you will need this extension to use Locations
\q
exit # go back to your normal user
```

## 3. Create virtual environment:
### 3.1 Most GNU/Linux and MacOS
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3.2 Windows
```bash
py -m venv venv
.\venv\Scripts\activate
```

## 4. Install `requirements.txt` inside virtual env:
```bash
pip3 install -r requirements.txt 
```

_See possible installation dependencies errors at the end of this document._

## 5. Create the database structure
```bash
python3 manage.py migrate
```
## 6. Create the first user
```bash
python3 manage.py createsuperuser
```
_Fill with some e-mail and password_
## 7. Fill the table "core_languages" with language list
This command will fetch language list from the server and then insert into the database.
```bash
python3 manage.py fillLanguageData
```

## (optional) Enable SSL for localhost
If you're running Djangology-CfMS in your localhost machine for development reasons you want to enable a SSL certificate in the Django Project and in your browser to avoid `urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed` (other way to do it is [disabling security certificate checks for requests in Python](https://www.geeksforgeeks.org/how-to-disable-security-certificate-checks-for-requests-in-python/), but in that case you could not test SSL features).

Source: https://medium.com/@millienakiganda/creating-an-ssl-certificate-for-localhost-in-django-framework-45290d905b88
1. Mkcert (cert and key filenames & domains configurable)
```bash
# install mkcert
sudo apt install libnss3-tools # install certutil dependency
curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
chmod +x mkcert-v*-linux-amd64
sudo cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert
mkcert -install
cd config/
mkcert -cert-file cert.pem -key-file key.pem 0.0.0.0 localhost 127.0.0.1 ::1
# RESTART BROWSER
```
2. Django-sslserver
```bash
pip install django-sslserver # with correct virtual environment already active
```
Add `sslserver` to `INSTALLED_APPS` in `djangoproject/frespo/settings.py`

## 6. Run backend server
```bash
./manage.py runserver
```
or with SSL
```bash
./manage.py runsslserver --certificate cert.pem --key key.pem  # correct file names if changes
```
	
## 7. Install and run frontend server
On `config` directory:
```bash
sudo apt install nodejs npm
sudo npm install grunt-cli -g
npm install
grunt build
```

# Optional extra set up
## Use another settings file
*  Copy `cp frespo/settings.py frespo/settings_dev.py` and
*  add the url to ALLOWED_HOSTS. There are two ways you can do that:
   * set the environment variable `DJANGO_SETTINGS_MODULE=frespo.settings_dev`; or
   * when running `manage.py` add `--settings=frespo.settings_dev` 

## Set up **PyCharm** to work with django applications.
Extracted from https://automationpanda.com/2017/09/14/django-projects-in-pycharm-community-edition/ :

From the Run menu, select Edit Configurations…. Click the plus button in the upper-left corner to add a Python configuration. Give the config a good name (like “Django: <command>”). Then, set Script to `manage.py` and Script parameters to the name and options for the desired Django admin command (like “runserver”). Set Working directory to the absolute path of the project root directory. Make sure the appropriate Python SDK is selected and the PYTHONPATH settings are checked. Click the OK button to save the config. The command can then be run from Run menu options or from the run buttons in the upper-right corner of the IDE window. You can add `--settings=frespo.settings_dev` there also
    
## Configure environment variables to make the application working.
You can configure it into PyCharm on `Run/Debug configurations > Environment > Environment variables > Click on the icon and add there the variables`. Now a list of some usefull variables:
```
GITHUB_APP_ID # The id to login with your github account
GITHUB_API_SECRET # The secret to login with your github account
```
	
#### Dependencies installations errors:

Look at https://gitlab.com/wikifunding/djangology-cfms/wikis/home#installing-on-new-environments for further information

* `ImportError: No module named _markerlib, Failed building wheel for distribute`:
	```
	easy_install distribute
	```

* `Failed building wheel for uWSGI`
	Update `requirements.txt` to use uWSGI version  2.0.15.
	 
* `ImportError: No module named unipath`
    ```
    pip install unipath 
    ```

# About name

Djangology is a jazz standard compositions made by [Django Reinhardt](http://en.wikipedia.org/wiki/Django_Reinhardt) who is the original guitarrist from the Django framework get [the name](http://www.djangobook.com/en/2.0/chapter01.html#django-s-history).

# Thanks

To FreedomSponsors developers and Free Software community involved in big projects like Python, Django and PostgreSQL that make possible this project. A special thanks goes out to Tony Lampada for [FreedomSponsors development](https://github.com/freedomsponsors/www.freedomsponsors.org).

# Licensing

This software is licensed under the [Affero General Public License](http://www.gnu.org/licenses/agpl-3.0.html). Take care of your users' freedom when running this software.
