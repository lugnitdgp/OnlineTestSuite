# OnlineTestSuite for Junior Code Cracker 

<p align="center">
  <a href="#">
    <img alt="logo" src=".github/jcclogo.png" width="140" />
  </a>
</p>

Activate a virtual environment in python using:
```shell
python3 -m venv venv
source venv/bin/activate
```


For debian based distro, in virtual evironment terminal type
```shell
pip install -r requirements.txt
```
### To run the project on local machine
Create a PostgresSQL database.</br>
Then `cp .env.example .env` and change `.env` file according to your need.

Inside project directory type
```shell
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```