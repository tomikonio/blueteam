FROM mysql:latest AS base
WORKDIR /app
EXPOSE 3306
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=weight
ENV MYSQL_USER=db
ENV MYSQL_PASSWORD=password
ENV RESTART=always
COPY weight-db.sql /docker-entrypoint-initdb.d/
