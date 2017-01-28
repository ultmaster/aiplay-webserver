# This dockerfile aims to create a aiplay webserver in the easiest way
# VERSION 1
# Author: ultmaster

FROM ubuntu:14.04
MAINTAINER ultmaster scottyugochang@hotmail.com

ENV DEBIAN_FRONTEND noninteractive

# Solve Dependencies first
COPY docker/sources.list /etc/apt/
RUN apt-get update
RUN apt-get -y install software-properties-common python-software-properties python python-dev python-pip
RUN apt-get -y install python3-software-properties python3 python3-dev python3-pip
RUN apt-get -y install gcc g++ git libtool python-pip libseccomp-dev cmake openjdk-7-jdk
RUN apt-get -y install nginx redis-server

# Download main code
RUN mkdir -p /var/www
RUN cd /var/www && git clone https://github.com/ultmaster/aiplay-webserver
RUN cd /aiplay-webserver

# Install judger
RUN useradd -r compiler
COPY docker/java_policy /etc
RUN chmod +x include/judger/runtest.sh
RUN include/judger/runtest.sh

RUN pip3 install -r requirements.txt
RUN /usr/bin/python3 setup.py

WORKDIR /var/www/aiplay-webserver
EXPOSE 4999

RUN chmod +x run.sh
CMD ./run.sh
