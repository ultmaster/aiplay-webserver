# This dockerfile is the common dependencies for webserver
# VERSION 1
# Author: ultmaster

FROM ubuntu:14.04
MAINTAINER ultmaster scottyugochang@hotmail.com
ENV DEBIAN_FRONTEND noninteractive

COPY docker/sources.list /etc/apt/
RUN apt-get update
RUN apt-get -y install software-properties-common python-software-properties python python-dev python-pip \
    python3-software-properties python3 python3-dev python3-pip gcc g++ git libtool python-pip libseccomp-dev \
    cmake openjdk-7-jdk nginx redis-server

CMD /bin/sh