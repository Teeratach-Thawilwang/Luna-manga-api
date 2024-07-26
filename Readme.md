# Index

- [Setup Project](#setup-project)
  - [1. Modify host url](#1-modify-host-url)
  - [2. Start docker container](#2-start-docker-container)
  - [3. Validate database connection](#3-validate-database-connection)
  - [4. Migrate table](#4-migrate-table)
  - [5. Seed initial data](#-5seed-initial-data)
  - [6. Create requirements file when install new package](#6-Create-requirements-file-when-install-new-package)
  - [7. Backup database](#7-backup-database)
- [Run unit test](#run-unit-test)
  - [1. Set APP_ENV](#1-set-app_env)
  - [2. Run test command](#2-run-test-command)
- [Docker command](#docker-command)
  - [1. Build image from Dockerfile](#1-build-image-from-dockerfile)
  - [2. Run image as a container from official image](#2-run-image-as-a-container-from-official-image)
  - [3. Run container from Dockerfile](#3-run-container-from-dockerfile)
  - [4. Push docker image](#4-push-docker-image)
  - [5. Common command](#5-common-command)

---

### [Setup Project](#index)

#### [1. Modify host url](#index)

##### For linux

```sh
# Add the following line in `/etc/hosts`
sudo nano /etc/hosts
127.0.0.1       api.dev.luna-manga.com
```

##### For Windows

```sh
# Open `C:\WINDOWS\system32\drivers\etc\hosts` (If there isn't one, just create it).
# Then add the following line.
127.0.0.1       api.dev.luna-manga.com
```

##### Now, you can use http://api.dev.luna-manga.com as your domain.

#### [2. Start docker container](#index)

```sh
copy .env.example to .env
docker-compose up -d --build
```

#### [3. Validate database connection](#index)

```sh
docker-compose exec db mariadb -u root -p     // password=root

# connect database
Host : WSL host, Get by using command "wsl hostname -I"
Port : 3306
User : root
Password : root
Database : dev
```

#### [4. Migrate table](#index)

```sh
# For first time, comment out "scheduler().handle()"
# In main/app/apps.py before run command.
# After migration success, bring "scheduler().handle()" back.
docker-compose exec app python manage.py makemigrations app
docker-compose exec app python manage.py migrate
```

#### [5. Seed initial data](#index)

```sh
docker-compose exec app python manage.py Seeds initial

"super user account"
email : super-user@email.com
password : super-user
// change password later in production.
```

#### [6. Create requirements file when install new package](#index)

```sh
docker-compose exec app pip freeze > requirements.txt
```

#### [7. Backup database](#index)

```sh
docker-compose exec <service_name> mysqldump -u [username] --password=[password]  [database_name] > [path/filename.sql]

# Example
docker-compose exec db mysqldump -u root --password=root  dev > backup_initial.sql
```

---

### [Run Unit Test](#index)

#### [1. Set APP_ENV](#index)

```sh
# This setting use sqlite as database.
APP_ENV=test
```

#### [2. Run test command](#index)

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

### [Docker command](#index)

#### [1. Build image from Dockerfile](#index)

```sh
docker build -t <any_image_name> .
```

#### [2. Run image as a container from official image](#index)

```sh
docker run --name <any_container_name> -i -d <image_name:tag>

# For example
docker run --name my-ubuntu -i -d ubuntu:23.10
docker run --name my-python -i -d python:3.11.3-buster
```

#### [3. Run container from Dockerfile](#index)

```sh
docker run -p 8080:8080 --name my-demo -i -d django-demo
```

#### [4. Push docker image](#index)

##### 1. Tag the image

```sh
docker tag [OPTIONS] IMAGE[:TAG] [REGISTRYHOST/][USERNAME/]NAME[:TAG]
# For example
docker tag ef56e8343d78 mydocker/my_image:0.1.0
```

##### 2. Push the image

```sh
docker push [REGISTRYHOST/][USERNAME/]NAME[:TAG]
# For example
docker push mydocker/my_image:0.1.0
```

#### [5. Common command](#index)

```sh
    service name คือชื่อ service container ใน docker-compose ไม่ใช่ container name

    # เรียกดู container ทั้งหมด
    docker ps -a

    # เรียกดู Image ทั้งหมด
    docker image list

    # start(ถ้ามีอยู่) หรือ re-create container ทั้งหมดใน mode detach หรือ background mode
    docker-compose up -d

    # สร้าง image ใหม่จาก Dockerfile และ re-create container ทั้งหมด
    docker-compose up -d --Build

    # สร้าง image ใหม่จาก Dockerfile และ re-create container ตาม service name ระบุ
    docker-compose up -d --build <service name>

    # start(ถ้ามีอยู่) หรือ re-create container โดยระบุ service name
    # และรันใน de detach หรือ background mode
    docker-compose up -d <service name>

    # start container
    docker-compose start <service name>

    # stop container คืน resource ให้เครื่อง
    docker-compose stop <service name>

    # เเช่เเข็ง container แต่ไม่คืน resource ให้เครื่อง
    docker-compose pause <service name>

    # restart container ทั้งหมดที่รันอยู่ เช่น เมื่อมีการแก้ไข env ต้อง restart ใหม่
    docker-compose restart

    # restart container ตาม service name ที่ระบุ
    docker-compose restart <service name>

    # shell เข้าไปใน container เหมือน ssh linux
    docker-compose exec <service name> bash

    # รัน command ใน container โดยไม่ต้อง shell เข้าไปใน container
    docker-compose exec <service name> <command>

    # ลบ Container ทั้งหมดที่ Stop อยู่
    docker rm $(docker ps -a -q)

    # ลบ Image ตามที่ระบุ
    docker rmi <image id>

    # หยุดการทำงาน Container ทั้งหมด
    docker stop $(docker ps -a -q)
```
