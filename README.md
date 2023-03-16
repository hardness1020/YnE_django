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
1.  - Set environment variable to true if you are running the app locally
      ```
      export TRAMPOLINE_CI=true
      ```
    - Or establish a connection from your local computer to your Cloud SQL instance for local testing purposes
      - Create another terminal and run the following command
        ```
        ./cloud_sql_proxy yne-django:asia-east1:yne-django
        ```
      - In orginal terminal
        ```
        export GOOGLE_CLOUD_PROJECT=yne-django
        export USE_CLOUD_SQL_AUTH_PROXY=true
        ```

2.  Run the following command to start the server
    ```
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver
    ```
    Then go to http://localhost:8000/ to see the app running


## 🔧 Running the Tests <a name = "tests"></a>

Run all the tests
```
python3 manage.py test
```

Run tests for a specific app
```
python3 manage.py test <app_name>
```


## 🚀 Deployment <a name = "deployment"></a>

Doc: https://cloud.google.com/python/django/flexible-environment#linuxmacos_2
```
gcloud app deploy
```


