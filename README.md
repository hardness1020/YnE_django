<!-- <p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p> -->

<h3 align="center">YnE</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

---

<p align="center"> Youthful activity, elderly pace.
    <br> 
</p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
- [🏁 Getting Started ](#-getting-started-)
  - [Prerequisites](#prerequisites)
- [🎈 Local Development ](#-local-development-)
- [🔧 Running the Tests ](#-running-the-tests-)
- [🚀 Deployment ](#-deployment-)
  - [Development ](#development-)
  - [Production ](#production-)
- [🎉 Acknowledgements ](#-acknowledgements-)

## 🧐 About <a name = "about"></a>

This is an back-end for YnE APP (Youth and Elderly). 
It is a web application that show the youth activities for the elderly.
It was deployed on Google APP Engine.

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites

Run the following command to install all the required packages.

```
pip3 install -r requirements.txt
```



## 🎈 Local Development <a name="usage"></a>
Doc: https://cloud.google.com/python/django/flexible-environment#linuxmacos_2
1.  - **Development on Local Machine SQLite Database**
        1.  Must **have** .env file in the root directory
    -  **Development on Google App Engine with cloud SQL**
        1.  Must **not have** .env file in the root directory
        2.  Select the project yne-django-dev and user account and then initiate authentication (setup once on your local machine)
            ``` 
            gcloud init
            gcloud auth application-default login
            ```
        3.  Establish a connection from your local computer to your Cloud SQL instance. 
            - Create another terminal and run the following command (download the cloud-sql-proxy from https://cloud.google.com/sql/docs/mysql/sql-proxy)
              ```
              ./cloud-sql-proxy yne-django-dev:asia-east1:yne-django-dev
              ```
            - In orginal terminal
              ```
              export GOOGLE_CLOUD_PROJECT=yne-django-dev
              export USE_CLOUD_SQL_AUTH_PROXY=true
              ```

2.  Run the following command to start the server
    ```
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py collectstatic
    python3 manage.py runserver
    ```
    Then go to http://localhost:8000/ to see the app running


## 🔧 Running the Tests <a name = "tests"></a>
1. Done first part of [Local Development ](#-local-development-).
2.  - Recommended to **use the debug toolbar to run the tests**
    - Or use CLI. Run all the tests
      ```
      python3 manage.py test
      ```

      Run tests for a specific app
      ```
      python3 manage.py test <app_name>
      ```


## 🚀 Deployment <a name = "deployment"></a>

Staging environment followed by: https://cloud.google.com/appengine/docs/legacy/standard/php/creating-separate-dev-environments

<!-- Doc: https://cloud.google.com/python/django/flexible-environment#linuxmacos_2 -->

<!-- ! Reset the environment variable to ensure that the app is deployed by the correct settings
```
export GOOGLE_CLOUD_PROJECT=yne-django
export USE_CLOUD_SQL_AUTH_PROXY=true
export SETTINGS_NAME=yne_django_settings
``` -->

### Development <a name = "development"></a>
Select the project yne-django-dev and user account
``` 
gcloud init
```
Create another terminal and run the following command
```
./cloud-sql-proxy yne-django-dev:asia-east1:yne-django-dev
```
Deploy the app
```
gcloud app deploy ./app-dev.yaml 
```

### Production <a name = "production"></a>
Select the project yne-django and user account
``` 
gcloud init
```
Create another terminal and run the following command
```
./cloud-sql-proxy yne-django:asia-east1:yne-django
```
Deploy the app
```
gcloud app deploy ./app-prod.yaml 
```

## 🎉 Acknowledgements <a name = "acknowledgement"></a>
- [Infrastructure](https://python.plainenglish.io/how-deploy-an-asgi-django-application-with-nginx-gunicorn-daphne-and-supervisor-on-ubuntu-server-dfd810f56274)


