FROM ubuntu:20.04

COPY pyflask/requirement.txt /
RUN apt-get update
RUN apt-get install -y python3 python3-pip mysql-client wget
RUN pip install -r requirement.txt

COPY docker/app/start.sh /

ENTRYPOINT /bin/bash start.sh
