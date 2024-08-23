#!/bin/bash/
sudo docker exec -it backend /bin/bash
python manage.py migrate
export DJANGO_SUPERUSER_USERNAME=Modestra
export DJANGO_SUPERUSER_PASSWORD=Terrarik22
export DJANGO_SUPERUSER_EMAIL="testuser@example.com"
python manage.py createsuperuser --noinput