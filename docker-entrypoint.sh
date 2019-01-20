export FLASK_APP=/code/show_image/__init__.py
flask initdb
gunicorn -w 4 -b 0.0.0.0:6666 show_image:app