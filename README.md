gitbash: source env\Scripts\activate
pip install django
pip install python-dotenv



To set an environment variable for production mode, you can use the following command in your terminal:
For Linux or macOS:

bash

export DJANGO_ENV=production



Yes, both **Nginx** and **Gunicorn** typically use **wsgi.py** in Django projects to serve the application. The `wsgi.py` file acts as an entry point for WSGI-compatible web servers (like Gunicorn) to communicate with your Django application.

Here's a typical setup:
1. **Nginx** acts as a reverse proxy, handling client requests, SSL, etc.
2. **Gunicorn** serves the Django application using `wsgi.py` to run the WSGI server.
   
Gunicorn starts Django's WSGI application (`wsgi.py`) to serve incoming requests.




sudo chown -R g2019supersam:www-data /home/g2019supersam/apps/zyxe/pro
python manage.py makemigrations authenticate
python mange.py migrate
python manage.py createsuperuser
export DJANGO_ENV=production
export DJANGO_SETTINGS_MODULE=pro.settings.production

edit .env
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl status gunicorn


g2019supersam@instance-20240908-083334:~/apps/zyxe/pro$ pwd
/home/g2019supersam/apps/zyxe/pro
g2019supersam@instance-20240908-083334:~/apps/zyxe/pro$ ls -la
total 288
drwxr-xr-x 7 g2019supersam www-data        4096 Sep 23 07:35 .
drwxr-xr-x 5 g2019supersam g2019supersam   4096 Sep 22 05:16 ..
-rw-r--r-- 1 g2019supersam www-data         262 Sep 23 05:16 .env
drwxr-xr-x 8 g2019supersam www-data        4096 Sep 23 05:17 .git
-rw-r--r-- 1 g2019supersam www-data         576 Sep 22 05:16 .gitignore
-rw-r--r-- 1 g2019supersam www-data         681 Sep 23 05:15 README.md
drwxr-xr-x 5 g2019supersam www-data        4096 Sep 23 07:31 authenticate
-rw-r--r-- 1 g2019supersam g2019supersam 122880 Sep 23 07:32 db.sqlite3
-rw-r--r-- 1 g2019supersam g2019supersam 122880 Sep 23 07:32 db2.sqlite3
srwxrwxrwx 1 g2019supersam www-data           0 Sep 23 07:35 gunicorn.sock
-rw-r--r-- 1 g2019supersam www-data         847 Sep 23 05:15 manage.py
drwxr-xr-x 4 g2019supersam www-data        4096 Sep 23 07:34 pro
drwxr-xr-x 4 g2019supersam www-data        4096 Sep 22 05:16 static
drwxr-xr-x 3 g2019supersam www-data        4096 Sep 22 05:16 templates


Note: gunicorn.sock
export DJANGO_ENV=production
python manage.py collectstatic      # Need to first export DJANGO_ENV=production
sudo systemctl reload nginx

Should be working.


Django's Interactive Shell:
python manage.py shell
from pro_profile.models import Profile
from authenticate.models import CustomUser  # If needed for user-related queries

user = CustomUser.objects.get(email="2019supersam@gmail.com")  # Fetch the user
profile = Profile.objects.create(user=user, address="123 Example St")

profile = Profile.objects.get(user=user)
