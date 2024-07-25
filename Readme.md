# Index

- Project setup
  - Modify Host URL
  - Start docker container with build image
  - Validate Database Connection
  - Migrate Table
  - Seed Initial Data
  - Create requirements file
  - Backup Database
- Run unit test
  - Set APP_ENV
  - Run test command
- Docker command
  - Build image from Dockerfile
  - Run image as a container from official image
  - Run container from Dockerfile
  - Run command in running container
  - Push docker image

---

## Project Setup

<br>

### Modify Host URL

#### For linux <br>

##### &emsp; Add the following line in `/etc/hosts`

```sh
sudo nano /etc/hosts
127.0.0.1       luna-manga-api.dev
```

#### For Windows <br>

##### &emsp; Open `C:\WINDOWS\system32\drivers\etc\hosts` (If there isn't one, just create it). Then add the following line.

```sh
127.0.0.1       luna-manga-api.dev
```

##### Now, you can use http://luna-manga-api.dev as your domain.

<br>

### Start docker container with build image option

```sh
copy .env.example to .env
docker-compose up -d --build
```

<br>

### Validate Database Connection

```sh
docker-compose exec db mariadb -u root -p     // password=root
```

<br>

### Migrate Table

```sh
# Do not forget to comment out "scheduler().handle()" in main/app/apps.py before run command.
# After migration success, Do not forget to bring "scheduler().handle()" back.
docker-compose exec app python manage.py makemigrations app
docker-compose exec app python manage.py migrate
```

<br>

### Seed Initial Data

```sh
docker-compose exec app python manage.py Seeds initial

"super user account"
email : super-user@email.com
password : super-user
// change password later in production.
```

<br>

### Connect Database

```sh
Host : WSL host, Get by using command "wsl hostname -I"
Port : 3306
User : root
Password : root
Database : dev
```

<br>

### Create requirements file

&emsp;If you install new python package into project, you need to update requirements file by following command.

```sh
docker-compose exec app pip freeze > requirements.txt
```

<br>

### Backup Database

```sh
docker-compose exec <service_name> mysqldump -u [username] --password=[password]  [database_name] > [path/filename.sql]

# Example
docker-compose exec db mysqldump -u root --password=root  dev > backup_initial.sql
```

<br>

---

## Run Unit Test

<br>

### Set APP_ENV

&emsp;This setting use sqlite as database."

```sh
change APP_ENV=test in .env
```

### Run Test

```sh
# run all test on API test
python manage.py test .

# run all test on app folder
python manage.py test app

# run test on specific test file
python manage.py test <path_to_file>

#Ex.1 - run specific service test
python manage.py test app.Domain.Customer.Services.Test_CustomerService

#Ex.2 - run specific API test
python manage.py test tests.backoffice.UserController.test_index
```

---

## Docker command

<br>

### Build image from Dockerfile

```sh
docker build -t <any_image_name> .
```

<br>

### Run image as a container from official image

```sh
docker run --name <any_container_name> -i -d <image_name:tag>
```

##### For example

```sh
docker run --name my-ubuntu -i -d ubuntu:23.10
docker run --name my-python -i -d python:3.11.3-buster
```

<br>

### Run container from Dockerfile

```sh
docker run -p 8080:8080 --name my-demo -i -d django-demo
```

<br>

### Run command in running container

```sh
docker-compose exec app python manage.py startapp myapp
docker-compose exec app pip install django mysqlclient
```

<br>

### Push docker image

#### 1. Tag the image

```sh
docker tag [OPTIONS] IMAGE[:TAG] [REGISTRYHOST/][USERNAME/]NAME[:TAG]
```

##### For example

```sh
docker tag ef56e8343d78 mydocker/my_image:0.1.0
```

<br>

#### 2. Push the image

```sh
docker push [REGISTRYHOST/][USERNAME/]NAME[:TAG]
```

##### For example

```sh
docker push mydocker/my_image:0.1.0
```
