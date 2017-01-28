# This dockerfile aims to create a aiplay webserver in the easiest way
# VERSION 1
# Author: ultmaster

FROM ubuntu:14.04
MAINTAINER ultmaster scottyugochang@hotmail.com
ENV DEBIAN_FRONTEND noninteractive

# Copy main code
RUN mkdir -p /var/www && cd /var/www && git clone https://github.com/ultmaster/aiplay-webserver
COPY setup.py /var/www/aiplay-webserver/
WORKDIR /var/www/aiplay-webserver

# Solve Dependencies first
COPY docker/sources.list /etc/apt/
RUN apt-get update
RUN apt-get -y install software-properties-common python-software-properties python python-dev python-pip \
    python3-software-properties python3 python3-dev python3-pip gcc g++ git libtool python-pip libseccomp-dev \
    cmake openjdk-7-jdk nginx redis-server

# Install judger
RUN useradd -r compiler
COPY include/judger/java_policy /etc/
RUN cd include/judger && chmod +x runtest.sh
RUN cd include/judger && ./runtest.sh

RUN pip3 install -r requirements.txt
RUN /usr/bin/python3 setup.py

EXPOSE 4999

RUN chmod +x run.sh
CMD ./run.sh
