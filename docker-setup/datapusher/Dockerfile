# See CKAN docs on installation from Docker Compose on usage
FROM ubuntu:18.04

# Install required system packages
RUN apt-get -q -y update \
    && DEBIAN_FRONTEND=noninteractive apt-get -q -y upgrade \
    && apt-get -q -y install \
        python3 \
        python3-dev \
        python3-pip \
        python3-wheel \
        libpq-dev \
        libxml2-dev \
        libxslt-dev \
        libxslt1-dev \
        libgeos-dev \
        libssl-dev \
        libffi-dev \
        zlib1g-dev \
        postgresql-client \
        build-essential \
        git-core \
        vim \
        wget \
        dos2unix \
        locales \
    && apt-get -q clean \
    && rm -rf /var/lib/apt/lists/*

RUN export LC_ALL="en_US.UTF-8" & export LC_CTYPE="en_US.UTF-8" & dpkg-reconfigure --frontend noninteractive locales


RUN git clone https://github.com/ckan/datapusher.git

RUN pip3 install -U pip && \
    pip3 install --upgrade setuptools && \
    pip3 install --upgrade werkzeug==0.16.0 && \
    pip3 install -r ./datapusher/requirements.txt && \
    pip3 install -e ./datapusher

CMD [ "python3", "datapusher/datapusher/main.py", "datapusher/deployment/datapusher_settings.py"]

