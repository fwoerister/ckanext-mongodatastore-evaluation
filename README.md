# Mongodatastore Evaluation
This repository contains all assets required to re-execute the evaluation part of the mastersthesis *Persistent Identification and Referencing of Evolving Research Data in Computational Experiments*. This covers:

* `docker-compose` files to setup the system under test
* A python framework for executing the functional and non-functional test cases
* Scripts to generate the diagrams, used in the evaluation part of the thesis

## Docker Setup
The folder `docker-setup` contains following docker-compose files:

| name                         | description |
| ---------------------------- | ----------- |
| `docker-compose.legacy.yml`  | Setup using the standard datastore implementation (based on PostgreSQL) |
| `docker-compose.yml`         | Setup using the novel datastore implementation based on a MongoDB (using 3shards) |
| `docker-compose.4shards.yml` | Setup using the novel datastore implementation based on a MongoDB (using 4shards) |
| `docker-compose.5shards.yml` | Setup using the novel datastore implementation based on a MongoDB (using 5shards) |
| `docker-compose.6shards.yml` | Setup using the novel datastore implementation based on a MongoDB (using 6shards) |

To start the complete system, execute this command:

```
docker-compose [--file docker-compose.[legacy|4shards|5shards|6shards].yml] up --build -d
```

__REMARK: Before executing the test cases, make sure that all services are up and running!__

## Running the Test Cases
For the test case execution this repository provides a own `Dockerfile`. This file takes care of installing required Python and R packages.

To run a testcase, first build the docker container

```
docker build -t evaluation .
```

Next, use following command to execute a specific test case:

```
docker run -it --network host -v results:/opt/evaluation/results  evaluation python run_testcases.py [TESTRUN TAG] --functional 1.1
```

## Generating the Diagrams
To generate the diagrams, put the result files from previous testruns into the charts folder and execute following command:

```
docker run -it --network host -v charts:/opt/evaluation/charts  [CONTAINER_NAME] python generate_diagrams.py
```

Each result file is named using the schema `[TEST RUN TAG]_[TEST CASE TAG]_result.csv` (e.g. `mdbshard03_nftc1_result.csv`)
Based on this tags the diagram generation script groups the results and renders the according diagrams as depicted in the thesis.


## Contact
Florian Wörister | florian.woerister[at]tuwien.ac.at