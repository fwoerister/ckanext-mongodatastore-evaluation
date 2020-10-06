FROM r-base:4.0.2

COPY . /opt/evaluation

RUN rm -rf /opt/evaluation/venv

ENV EVAL_HOME /opt/evaluation

# Create eval user
RUN useradd -r -u 900 -m -c "eval account" -d $EVAL_HOME -s /bin/false eval

RUN apt-get -q -y update \
    && DEBIAN_FRONTEND=noninteractive apt-get -q -y upgrade \
    && apt-get -q -y install \
        python3 \
        python3-dev \
        python3-pip \
        python3-virtualenv \
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
        libcurl4-openssl-dev \
        default-jdk \
        dos2unix \
    && apt-get -q clean \
    && rm -rf /var/lib/apt/lists/*

# create virtual python environment
RUN mkdir -p "$EVAL_HOME"/venv && \
    python3 -m virtualenv -p python3 "$EVAL_HOME"/venv && \
    ln -s "$EVAL_HOME"/venv/bin/pip /usr/local/bin/eval-pip &&\
    ln -s "$EVAL_HOME"/venv/bin/python /usr/local/bin/eval-python

RUN eval-pip install -r "$EVAL_HOME"/requirements.txt

# install required R packages
RUN Rscript "$EVAL_HOME"/install_r_packages.r

# prepare entrypoint.sh
RUN dos2unix "$EVAL_HOME"/entrypoint.sh
RUN chmod +x "$EVAL_HOME"/entrypoint.sh

ENTRYPOINT ["/opt/evaluation/entrypoint.sh"]
CMD ["python","run_testcases.py", "test"]