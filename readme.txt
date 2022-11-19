You need Python 3.8, make an environment of same and activate it. Then -> pip install -r requirements.txt
Go to the project root directory where manage.py is placed.
1./manage.py makemigrations
2./manage.py migrate
Although migrations are run already on the connected database

3../manage.py runserver 8000


Reminder Management Command is ./manage.py reminder




For Reminder Command
In crontab -e , write 0 21 * * *  (path to python interpreter)  (path to manage.py) reminder
