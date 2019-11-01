FROM debian:stretch
MAINTAINER "Marten van Dijk"

RUN \
  apt-get update && \
  apt-get install -y python3-pip && \
  pip3 install flask && \
  mkdir /root/templates

COPY run /root/run
COPY templates/hello_world.html /root/templates/hello_world.html
COPY flasktest.py /root/flasktest.py

EXPOSE 5000
CMD bash /root/run
