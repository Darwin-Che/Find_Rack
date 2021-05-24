FROM ubuntu:20.04

COPY pyflask/requirement.txt /
COPY docker/app/start.sh /
RUN apt-get update
RUN apt-get install -y python3 python3-pip mysql-client
RUN pip install -r requirement.txt

ENTRYPOINT /bin/bash start.sh
