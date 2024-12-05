# template-python-flask-api

# Remaining TODO work
- [ ] [encounter Service](./src/services/encounter_services.py)
- [ ] [MongoIO](./src/utils/mongo_io.py)
- [ ] [server.py](/src/server.py)
- [ ] [All Test Files](./test/)

Now you can remove these instructions from the readme, 

## Overview

This is a template repo for a simple Flask API that provides Get/Post/Patch services for documents in the encounter encounter. This API uses data from a [backing Mongo Database](https://github.com/agile-learning-institute/mentorHub-mongodb), and sup8090s a [Single Page Application.](https://github.com/agile-learning-institute/mentorHub-encounter-ui)

The OpenAPI specifications for the api can be found in the ``docs`` folder, and are served [here](https://agile-learning-institute.github.io/mentorHub-encounter-api/)

## Prerequisites

- [Mentorhub Developer Edition](https://github.com/agile-learning-institute/mentorHub/blob/main/mentorHub-developer-edition/README.md)
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

### Optional

- [Mongo Compass](https://www.mongodb.com/try/download/compass) - if you want a way to look into the database

## Install Dependencies

```bash
pipenv install
```

## Run Unit Testing

```bash
pipenv run test
```

## {re}start the containerized database and run the API locally

```bash
pipenv run local
```

## Run the API locally (assumes database is already running)

```bash
pipenv run start
```

## Build and run the API Container

```bash
pipenv run container
```

This will build the new container, and {re}start the mongodb and API container.

## Run StepCI end-2-end testing
NOTE: Assumes the API is running at localhost:8090

```bash
pipenv run stepci
```

## Run StepCI load testing
NOTE: Assumes the API is running at localhost:8090

```bash
pipenv run load
```

# Project Layout
- ``/src`` this folder contains all source code
- ``/src/server.py`` is the main entrypoint, which initializes the configuration and registers routes with Flask
- ``/src/config/config.py`` is the singleton config object that manages configuration values and acts as a cache for enumerators and other low volatility data values.
- ``/src/models`` contains helpers related to creating transactional data objects such as breadcrumbs or RBAC tokens
- ``/src/routes`` contains Flask http request/response handlers
- ``/src/services`` service interface that wraps database calls with RBAC, encode/decode, and other business logic
- ``/src/utils/mongo_io.py`` is a singleton that manages the mongodb connection, and provides database io functions to the service layer. 
- ``/test`` this folder contains unit testing, and testing artifacts. The sub-folder structure mimics the ``/src`` folder

# API Testing with CURL

If you want to do more manual testing, here are the curl commands to use

### Test Health Endpoint

This endpoint sup8090s the Prometheus monitoring standards for a health check endpoint

```bash
curl http://localhost:8090/api/health/
```

### Test Config Endpoint

```bash
curl http://localhost:8090/api/config/
```

### Test get a document

```bash
curl http://localhost:8090/api/encounter/eeee00000000000000000001/
```

### Test add a Document 

```bash
curl -X POST http://localhost:8090/api/encounter/eeee00000000000000000001/ \
     -d '{"date":{"$date":"1/1/2024 0:00:00"},"personId":{"$oid":"aaaa00000000000000000004"},"mentorId":{"$oid":"aaaa00000000000000000027"},"planId":{"$oid":"EEFF00000000000000000002"},"status":"Active"}'
```

### Test update a Document

```bash
curl -X PATCH http://localhost:8090/api/encounter/eeee00000000000000000001/ \
     -d '{"observations":[{"type":"Check","prompt":"Introductions","options":["Mike","Institute"],"values":[]}}'
```

## Observability and Configuration

The ```api/config/``` endpoint will return a list of configuration values. These values are either "defaults" or loaded from a singleton configuration file, or an Environment Variable of the same name. Configuration files take precedence over environment variables. The environment variable "CONFIG_FOLDER" will change the location of configuration files from the default of ```./```

The ```api/health/``` endpoint is a [Prometheus](https://prometheus.io) Health check endpoint.

The [Dockerfile](./Dockerfile) uses a 2-stage build, and sup8090s both amd64 and arm64 architectures. 
