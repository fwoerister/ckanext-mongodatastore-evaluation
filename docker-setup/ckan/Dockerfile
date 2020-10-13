# See CKAN docs on installation from Docker Compose on usage
FROM ubuntu:20.04

# Install required system packages
RUN ln -fs /usr/share/zoneinfo/Europe/Vienna /etc/localtime
RUN apt-get -q -y update \
    && DEBIAN_FRONTEND=noninteractive apt-get -q -y upgrade \
    && apt-get -q -y install \
        python3 \
        python3-dev \
        python3-pip \
        python3-virtualenv \
        python3-wheel \
        libpq-dev \
        libxml2-dev \
        libxslt-dev \
        libgeos-dev \
        libssl-dev \
        libffi-dev \
        postgresql-client \
        build-essential \
        git-core \
        vim \
        wget \
        dos2unix \
    && apt-get -q clean \
    && rm -rf /var/lib/apt/lists/*
RUN dpkg-reconfigure --frontend noninteractive tzdata

# Define environment variables
ENV CKAN_HOME /usr/lib/ckan
ENV CKAN_VENV $CKAN_HOME/venv
ENV CKAN_CONFIG /etc/ckan
ENV CKAN_STORAGE_PATH=/var/lib/ckan

# Build-time variables specified by docker-compose.yml / .env
ARG CKAN_SITE_URL

# Create ckan user
RUN useradd -r -u 900 -m -c "ckan account" -d $CKAN_HOME -s /bin/false ckan

# Setup virtual environment for CKAN
RUN mkdir -p $CKAN_VENV $CKAN_CONFIG $CKAN_STORAGE_PATH && \
    python3 -m virtualenv -p python3 $CKAN_VENV && \
    ln -s $CKAN_VENV/bin/pip3 /usr/local/bin/ckan-pip &&\
    ln -s $CKAN_VENV/bin/ckan /usr/local/bin/ckan

# Setup CKAN
RUN ckan-pip install setuptools==44.1.0
RUN ckan-pip install --upgrade pip
RUN ckan-pip install -e 'git+https://github.com/fwoerister/ckan.git@5632-fixReloaderOption#egg=ckan[requirements]'

COPY ckan/ckan-entrypoint.sh ./ckan-entrypoint.sh
RUN dos2unix ./ckan-entrypoint.sh
COPY ckan/cred.json /etc/ckan/cred.json
RUN ckan-pip install -U pip && \
    ckan-pip install --upgrade --no-cache-dir -r $CKAN_VENV/src/ckan/requirements.txt && \
    ln -s $CKAN_VENV/src/ckan/ckan/config/who.ini $CKAN_CONFIG/who.ini && \
    chmod +x /ckan-entrypoint.sh && \
    chown -R ckan:ckan $CKAN_HOME $CKAN_VENV $CKAN_CONFIG $CKAN_STORAGE_PATH

# install dcat plugin
RUN ckan-pip install -e git+https://github.com/ckan/ckanext-dcat.git@6b7ec505f303fb18e0eebcebf67130d36b3dca82#egg=ckanext-dcat
RUN ckan-pip install -r /usr/lib/ckan/venv/src/ckanext-dcat/requirements.txt

# install archiveview plugin
RUN ckan-pip install -e git+https://github.com/fwoerister/ckanext-archiveview.git@v0.0.2#egg=ckanext-archiveview
RUN ckan-pip install -r /usr/lib/ckan/venv/src/ckanext-archiveview/requirements.txt

# install mongodatastore plugin
RUN ckan-pip install -e git+https://github.com/fwoerister/ckanext-mongodatastore.git@v0.4#egg=ckanext-mongodatastore
RUN ckan-pip install -r /usr/lib/ckan/venv/src/ckanext-mongodatastore/requirements.txt

RUN ckan-pip install flask-debugtoolbar

USER ckan
EXPOSE 5000

ENTRYPOINT ["/ckan-entrypoint.sh"]
CMD ["ckan","-c","/etc/ckan/production.ini", "run", "--host", "0.0.0.0", "--disable-reloader"]
