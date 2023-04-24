sudo docker tag redis:latest gcr.io/yne-django-dev/redis:latest
sudo docker tag yne_django-web:latest gcr.io/yne-django-dev/yne_django-web:latest
sudo docker tag yne_django-daphne:latest gcr.io/yne-django-dev/yne_django-daphne:latest
sudo docker tag yne_django-nginx:latest gcr.io/yne-django-dev/yne_django-nginx:latest
sudo docker push gcr.io/yne-django-dev/redis:latest
sudo docker push gcr.io/yne-django-dev/yne_django-web:latest
sudo docker push gcr.io/yne-django-dev/yne_django-daphne:latest
sudo docker push gcr.io/yne-django-dev/yne_django-nginx:latest