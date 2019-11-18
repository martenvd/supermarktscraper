FROM debian:stretch
MAINTAINER "Marten van Dijk"

RUN \
  apt-get update && \
  apt-get install -y python3-pip && \
  pip3 install flask flask-session mysql-connector-python


COPY run /root/run
COPY templates /root/templates
COPY flask-test.py /root/flask-test.py
COPY static /root/static

EXPOSE 5000
CMD bash /root/run
