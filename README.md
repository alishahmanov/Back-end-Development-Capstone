# Back-end Development Capstone

Djirection is a Django site for viewing songs, concert photographs, and concert details. Users can sign in and record their attendance, and staff can manage concerts in Django Admin.

Install dependencies with `pip install -r requirements.txt`, apply migrations with `python manage.py migrate`, then run `python manage.py runserver`. Create an admin with `python manage.py createsuperuser`. The Songs and Pictures API origins can be configured with `SONGS_URL` and `PICTURES_URL`.

Build the development image with `docker build -t djangoserver:capstone .`. The image serves port 8000. The included Kubernetes Deployment expects the image to be available on the cluster and can be applied with `kubectl apply -f deployment.yml`. Set the service origins for the target environment before deploying.
