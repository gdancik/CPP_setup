FROM mysql:8.0
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=dcast
RUN apt-get update && apt-get install -y vim
ADD my.cnf /etc/mysql/my.cnf
ADD dcast_dump_2019-03-26.sql /docker-entrypoint-initdb.d

