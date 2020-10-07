FROM mongo:4.4.0-bionic

RUN apt-get -q -y update \
    && apt-get -q -y install dos2unix

ADD ./scripts /scripts

RUN dos2unix /scripts/*