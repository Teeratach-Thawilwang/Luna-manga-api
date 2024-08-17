
call docker-compose up -d --build
call docker tag luna_manga_api teeratachdocker/luna_manga_api:latest
call docker push teeratachdocker/luna_manga_api:latest