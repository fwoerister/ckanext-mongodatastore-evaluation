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

__REMARK: Before running the docker-compose file, rename the file `.env-template` to `.env`__

__REMARK: Due to the fact, that the datapusher is running inside a container, the base_url of the CKAN instance has to be set to the container name (i.e. http://ckan:5000). Therefore this hostname has to be added to the hosts file before execution of the test cases. (/etc/hosts for linux systems and C:\Windows\system32\drivers\etc\hosts for Windows systems)__

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
docker run -it --network host -v `pwd`/results:/opt/evaluation/results  evaluation python run_testcases.py functional --functional
```

To only execute the functional test cases use the argument `--functional`. This argument also accepts a list of test case numbers, e.g. `--functional 1.1 2.1 3.2`. To execute specific non-functional test cases, use the `--nonfunctional 1 2` switch.

Available test cases:

### Functional:

| Identify  | Descripition |
| --------  | -------------|
| 1.1       | Upload of a CSV file to the repository along with its metadata             |
| 2.1       | Inserting new records to an CKAN resource             |
| 2.2       | Modification of a record in an CKAN resource             |
| 2.3       | Deletion of a record in an CKAN resource            |
| 3.1       | Querying the current state of an CKAN resource by exact value             |
| 3.2       | Querchying the current state of an CKAN resource by defining a range on a specific field (range query)             |
| 3.3       | Fulltext Query on an CKAN resource            |
| 3.4       | Query with defined sort order on an CKAN resource             |
| 4.1       | Creation and retrieval of an persistently identified subset of an CKAN resource (defined by an exact filter condition)             |
| 4.2       | Creation and retrieval of an persistently identified subset of an CKAN resource (defined by range query)             |
| 4.3       | Creation and retrieval of an persistently identified subset of an CKAN resource (defined by fulltext query)             |
| 4.4       | Creation and retrieval of an persistently identified subset of an CKAN resource (defined query with sort order)             |
| 5.1       | Persistently identify an computational experiment and the datasubset (using the REST API) it is based on + Publishing of both PIDs in CKAN along with related metadata             |
| 5.2       | Persistently identify an computational experiment and the datasubset (using the CLI tool) it is based on + Publishing of both PIDs in CKAN along with related metadata             |

### Non-Functional:

| Identify  | Descripition |
| --------  | -------------|
| 1         | Examine the Query Response Time on Current State |
| 2         | Examing the Query Response Time on Non-Versioned MongoDB Collections             |
| 3         | Examine Retrieval Time of Stored Queries              |
| 4         | Examine the Impact of Indexing              |

## Generating the Diagrams
To generate the diagrams, put the result files from previous testruns into the charts folder and execute following command:

```
docker run -it --network host -v charts:/opt/evaluation/charts  [CONTAINER_NAME] python generate_diagrams.py
```

Each result file is named using the schema `[TEST RUN TAG]_[TEST CASE TAG]_result.csv` (e.g. `mdbshard03_nftc1_result.csv`)
Based on this tags the diagram generation script groups the results and renders the according diagrams as depicted in the thesis.


## Contact
Florian Wörister | florian.woerister[at]tuwien.ac.at
