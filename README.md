# Edu-Exam

Edu-Exam is a **backend application** designed to support an online examination system.

## 🚀 Installation & Setup

#### Prerequisites
- **Python version:** 3.14

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/javasxz/edu-exam
$ cd edu-exam
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3 -m venv venv
$ source venv/bin/activate
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
Once the server is running, navigate to `http://127.0.0.1:8000/api/v1/`.

## 📊 Load Initial Data
To populate the database with sample or default data, run:
```sh
python manage.py populatedata
```
