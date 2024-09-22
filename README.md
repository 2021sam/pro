


To set an environment variable for production mode, you can use the following command in your terminal:
For Linux or macOS:

bash

export DJANGO_ENV=production



Yes, both **Nginx** and **Gunicorn** typically use **wsgi.py** in Django projects to serve the application. The `wsgi.py` file acts as an entry point for WSGI-compatible web servers (like Gunicorn) to communicate with your Django application.

Here's a typical setup:
1. **Nginx** acts as a reverse proxy, handling client requests, SSL, etc.
2. **Gunicorn** serves the Django application using `wsgi.py` to run the WSGI server.
   
Gunicorn starts Django's WSGI application (`wsgi.py`) to serve incoming requests.

