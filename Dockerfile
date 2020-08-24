FROM ubuntu:bionic

RUN suod apt-get update && sudo apt-get upgrade && sudo apt-get install libcurl4-openssl-dev r-cran-rjava