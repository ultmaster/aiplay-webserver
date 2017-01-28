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
RUN cd /tmp && git clone https://github.com/ultmaster/aiplay-webserver

# Install judger
RUN useradd -r compiler
COPY docker/java_policy /etc
RUN cd aiplay-webserver && include/judger/runtest.sh

RUN pip3 install -r requirements.txt

HEALTHCHECK --interval=5s --retries=3 CMD python /code/service.py
WORKDIR /code
EXPOSE 4999
CMD /bin/bash /code/run.sh