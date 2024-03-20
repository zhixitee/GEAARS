![Forks](https://img.shields.io/badge/forks-0-blue)
![Stars](https://img.shields.io/badge/clone-6-yellow)

# GEAARS(Glasgow Events And Arts Review System)

## Description

Welcome to WAD group project setup by team 8D . This is a Event review website hardcoded in python and the Django framework. This website aim in showcasing the latest events happening around in Glasgow in which they can later leave the review for the performance. With this website users can definitely get to know about the events happening around the town. In this users can be both event organiser as well where this website through admin allow their Events post on the website which later can be reviewed by the organisers or the performer through the site. We hope you like the work.

## Installation Instructions

1. Change directory to GEAARS folder where it contains manage.py file (command - ls GEAARS) this will tell about the contents of the folder.

2. 

```
conda create --name events
```

(This command creates the virtual environment name events)

3. 

```
conda activate events
```

(The command to activate the environment)

4. 

```
   pip install django==2.2.28
```

   (This version of django is used in this website development)

5. 

```
pip install pillow
```

(This format is used to manipulate and save many different image formats)


6. 

```
python manage.py makemigrations
```

(This command is used to automatically make migrations to files that have been changed to make models and updating the database schema) 

7. 

```
python manage.py migrate
```

(This command makes sure that the schema matches the current state of the current models,managing the database changes throughout the lifecycle.)

8. 

```
python populate_events.py
```

(This command makes sure that the database is populated properly)

9. 

```
python manage.py runserver
```

(For running the server )  

## General Instructions
1. Fork this repository
2. Clone the forked repository
3. Add your contributions(if any)
4. Run the server check the changes.
5. Commit and push.
6. Wait for pull request to be merged.
