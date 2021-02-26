git pull
docker-compose build web
docker-compose run web python manage.py migrate
docker-compose up --no-deps -d web