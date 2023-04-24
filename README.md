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
  - [Prerequisites ](#prerequisites-)
- [🎈 Local Development ](#-local-development-)
- [🚀 Deployment ](#-deployment-)
- [🎉 Acknowledgements ](#-acknowledgements-)

<br/>

## 🧐 About <a name = "about"></a>

This is an back-end for YnE APP (Youth and Elderly). 

It is a web application that show the youth activities for the elderly.

<br/>

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites <a name = "prerequisites"></a>

- Run the following command to install all the required packages.
  ```
  pip3 install -r requirements.txt
  ```
- Not have .env file in the root directory
- Download the project key from Google Cloud Platform and put it in the /keys directory
- Download [docker-compose](https://docs.docker.com/compose/install/). Suggestion to use scenario two or directly download from github.

<br/>

## 🎈 Local Development <a name="usage"></a>
The [prerequisties](#prerequisites-) must be done before running the following commands.

1.  Select the project yne-django-dev and user account and then initiate authentication (setup once on your local machine)
    ```
    gcloud init
    gcloud auth application-default login
    ```

2.  Build the container for each service and a connection from your local computer to Cloud SQL instance. 
    ```
    docker-compose up -d
    ```
    - The port 1337 is used for outside connection to the server ([127.0.0.1:1337](http://127.0.0.1:1337/))

3.  If you want to establish the tables in the database, run the code in the web container.
    ```
    docker exec -it yne-django-dev_web_1 bash
    ```
    ```
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py collectstatic
    ```
    

<br/>

<!-- ## 🔧 Running the Tests <a name = "tests"></a>
1.  - Recommended to **use the debug toolbar to run the tests**
    - Or use CLI. Run all the tests
      ```
      python3 manage.py test
      ```

      Run tests for a specific app
      ```
      python3 manage.py test <app_name>
      ```

<br/> -->

## 🚀 Deployment <a name = "deployment"></a>
> If you are running docker as root (i.e. with sudo docker), then make sure to configure the authentication as root. [Link](https://stackoverflow.com/questions/55446787/permission-issues-while-docker-push)

Select the project yne-django-\<dev_or_prod> and user account
```
gcloud auth login
gcloud config set project yne-django-<dev_or_prod>
gcloud auth configure-docker
```

Push the four images to Google Container Registry
```
docker-compose build

docker tag <IMAGE_NAME>:latest gcr.io/yne-django-<dev_or_prod>/<IMAGE_NAME>:latest
docker push gcr.io/yne-django-<dev_or_prod>/<IMAGE_NAME>:latest
```

<br/>

## 🎉 Acknowledgements <a name = "acknowledgement"></a>
- [Google Cloud Staging Environment](https://cloud.google.com/appengine/docs/legacy/standard/php/creating-separate-dev-environments)
  


