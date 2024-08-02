
call docker-compose up -d --build
docker tag luna_manga_api teeratachdocker/luna_manga_api:latest
docker push teeratachdocker/luna_manga_api:latest