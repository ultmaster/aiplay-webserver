# This dockerfile aims to create a aiplay webserver in the easiest way
# VERSION 1
# Author: ultmaster

FROM aiplay/server_base:v1
MAINTAINER ultmaster scottyugochang@hotmail.com
ENV DEBIAN_FRONTEND noninteractive

# Copy main code
RUN mkdir -p /var/www/aiplay-webserver
COPY . /var/www/aiplay-webserver/
WORKDIR /var/www/aiplay-webserver

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
