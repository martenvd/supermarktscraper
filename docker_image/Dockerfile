FROM debian:stretch
MAINTAINER "Marten van Dijk"

RUN \
  echo "apt update" && \
  apt-get update && \
  echo "install mariaDB" && \
  apt-get install -y mysql-server

COPY run /root/run
COPY mysql.sql /root/mysql.sql
COPY 50-server.cnf /etc/mysql/mariadb.conf.d/50-server.cnf

EXPOSE 3306
CMD bash /root/run
