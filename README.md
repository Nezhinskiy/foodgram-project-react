# Foodgram - a social network about cooking with a shopping list upload

![example workflow](https://github.com/Nezhinskiy/foodgram-project-react/actions/workflows/foodgram-project-react_workflow.yml/badge.svg)

[Go to site](http://footgram.ru/recipes)

[API documentation](http://footgram.ru/docs/redoc.html)

[Go to API](http://footgram.ru/api)

## Description:
The site is a database of culinary recipes. Users can create their own recipes, read other users' recipes, subscribe to interesting authors, add the best recipes to favorites, and create a shopping list and download it in txt format. There is also a docker-compose file that allows you to quickly deploy a database container (PostgreSQL), a django + gunicorn project container, and an nginx container.

## Technologies:
Python 3, Django, Django Rest Framework, Docker, Docker-Compose, Gunicorn, NGINX, PostgreSQL, Digital Ocean, Continuous Integration, Continuous Deployment

## Deploy project to remote server:
- Clone repository:
```
https://github.com/Nezhinskiy/foodgram-project-react.git
```

- Install Docker and Docker Compose on the server (for ubuntu):

```
sudo apt install curl                                   # installing a file download utility
curl -fsSL https://get.docker.com -o get-docker.sh      # download script for installation
sh get-docker.sh                                        # running the script
sudo apt-get install docker-compose-plugin              # install docker compose
```

- Copy the docker-compose.yml file and the nginx directory from the infra directory to the server (execute commands while in the infra directory):
```
scp docker-compose.yml username@IP:/home/username/   # username - server username
scp -r nginx username@IP:/home/username/             # IP - server public IP
```

- To work with GitHub Actions, you need to create environment variables in the Secrets > Actions section of the repository:
```
DEBUG=False             # Django debug
DEBUG_MODE              # "False" for PostgreSQL, "True" for SQLite 
DOCKER_PASSWORD         # Docker Hub password
DOCKER_USERNAME         # Docker Hub login
HOST                    # server public IP
USER                    # server username
PASSPHRASE              # *if ssh key is password protected
SSH_KEY                 # private ssh key
TELEGRAM_TO             # Telegram account ID to send a message
TELEGRAM_TOKEN          # token of the bot sending the message
DB_ENGINE               # "django.db.backends.postgresql"
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (default port)
```

- Create and run Docker containers, run command on server:
```
sudo docker-compose up -d
```

- After a successful build, run the migrations:
```
sudo docker compose exec backend python manage.py migrate
```

- Create superuser:
```
sudo docker compose exec backend python manage.py createsuperuser
```

- Collect static:
```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

- Fill the database with content from the ingredients.json and tags.json files:
```
sudo docker compose exec backend python manage.py load_data
```

- For stopping Docker containers:
```
sudo docker compose down -v      # with removal
sudo docker compose stop         # without removal
```

## After each update of the repository (push to the master branch), the following will happen:

1. Checking the code for compliance with the PEP8 standard (using packages: flake8 pep8-naming flake8-broken-line flake8-return flake8-isort)
2. Building and delivering [frontend](https://hub.docker.com/repository/docker/nezhinsky/foodgram-project-react) and [backend](https://hub.docker.com/repository/docker/nezhinsky/foodgram-project-backend) docker images to [my Docker Hub](https://hub.docker.com/u/nezhinsky)
3. Deploying a project on a remote server
4. Sending a message to Telegram if successful

## Running the project on the local machine:

- Clone repository:
```
https://github.com/Nezhinskiy/foodgram-project-react.git
```

- Go to infra directory:
```
cd foodgram-project-react/infra/
```

- Create an .env file in the infra directory and fill it with your data:
```
DEBUG=False             # Django debug
DEBUG_MODE              # "False" for PostgreSQL, "True" for SQLite 
DB_ENGINE               # "django.db.backends.postgresql"
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (default port)
```

- Create and run Docker containers, sequentially run the commands to create migrations, collect statics, create a superuser, as indicated above.
```
sudo docker-compose up
```

- After the launch, the project will be available at: [http://localhost/](http://localhost/)

- Documentation will be available at: [http://localhost/docs/redoc.html](http://localhost/docs/redoc.html)


### Author:
Mikhail Nezhinsky (c) 2023

Linkedin - https://www.linkedin.com/in/mikhail-nezhinsky/