🔎🚀 **Amazon Daily Automatic Web Crawler**

## Technology Stack
1. Python 🐍
2. Django 🎸
3. Redis 🔄
4. Celery 🌼
5. Celery-Beat ⏰
6. Docker 🐳
7. docker-compose 📦
8. Git/GitHub 🐙

## Some Important Files
1. `requirements.txt` (Contains all Python required libraries)
2. `docker-compose.yml` (Contains the Docker configuration for the application)
3. `Dockerfile` (Contains the build configuration for the environment)
4. `file-structure.txt` (Provides the file structure of the project)

## Important Command
To start the project, run the following command from the root directory:
```
docker-compose up --build
```

Access your project at:
```
http://localhost:8000/
```

### Remember
1. Docker must be installed on your system to run this project.
2. Set `DEBUG` in `settings.py` to `True` during development, otherwise set it to `False`.
3. If you are running the command for the first time, close it by pressing `Ctrl + C` and rerun the command.

## Features
1. Automatically collects data at 12:00 AM (IST) daily.
2. Ability to add new links.
3. Categorization support with the option to add any number of links under each category.
4. Download the generated CSV file at any time by visiting the respective product link.
5. Enable/disable data collection for each link using the provided radio button.

🙌 **Contributors**
- [Sanskar Goyal](https://github.com/Sanskargoyal608)
- [Vivek Raj Gupta](https://github.com/Vivek-raj-gupta-2002)
