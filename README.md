![Forks](https://img.shields.io/github/forks/<username>/<repository>?style=social)
![Stars](https://img.shields.io/github/stars/<username>/<repository>?style=social)

# GEAARS (Glasgow Events And Arts Review System)

## Description

GEAARS, developed by Team 8D, is a comprehensive event review platform designed with Python and the Django framework. It serves as a central hub for discovering and reviewing events in Glasgow. Users can find details about upcoming events and share their experiences through reviews. The platform also caters to event organizers, allowing them to post and manage events, thereby fostering a vibrant community around Glasgow's cultural scene.

## Features

- **Event Discovery:** Browse the latest events in Glasgow, including concerts, exhibitions, and more.
- **Reviews:** Share and read reviews of events to gauge experiences and expectations.
- **Organizer Portal:** Event organizers can post and manage their events, reaching a wider audience.

## Installation Instructions

Ensure you have Conda and Python installed on your system before proceeding.

1. **Clone the Repository**

```bash
git clone < https://github.com/zhixitee/GEAARS.git >
cd GEAARS
```

2. **Create and Activate a Virtual Environment**

```bash
conda create --name GEAARS python=3.8
conda activate GEAARS
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Database Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Populate the Database**

```bash
python populate_events.py
```

6. **Run the Server**

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your web browser to access the application.

## Contribution Guidelines

1. Fork this repository.
2. Clone your forked repository to your local machine.
3. Make your changes and test them locally.
4. Commit your changes with a clear commit message.
5. Push your changes to your fork.
6. Submit a pull request to the original repository.
7. Wait for your pull request to be reviewed and merged.

## Acknowledgments

- Google Maps API for event location features.
- Bootstrap for responsive design and UI components.

## Team 8D Members

- Alan Gardiner
- Callum Neilson
- Edan Hymes
- Saksham Thukral
- Tareq Lgried
- Zhi Xi Tee

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.