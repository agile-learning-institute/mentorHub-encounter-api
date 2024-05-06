# encounter-api

## Overview

This is a simple Flask API that provides Get/Post/Patch services for docuements in the Encounter collection. This API uses data from a [backing Mongo Database](https://github.com/agile-learning-institute/mentorHub-mongodb), and supports a [Single Page Application.](https://github.com/agile-learning-institute/mentorHub-encounter-ui)

The OpenAPI specifications for the api can be found in the ``docs`` folder, and are served [here](https://agile-learning-institute.github.io/mentorHub-encounter-api/)

## Prerequisits

- [Mentorhub Developer Edition](https://github.com/agile-learning-institute/mentorHub/blob/main/mentorHub-developer-edition/README.md)
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

### Optional

- [Mongo Compass](https://www.mongodb.com/try/download/compass) - if you want a way to look into the database

## Install Flask Dependencies

```bash
pipenv install
```

<!-- ## Run Unit Testing

```bash
make test
``` -->

## Run the API locally

```bash
pipenv run local
```

Serves up the API locally with a backing mongodb database, ctrl-c to exit

## Build the API Container

```bash
pipenv run container
```

This will build the new container, and start the mongodb and API container ready for testing. <!--The test script ./test/test.sh is also run so you should see information about an inserted document. You will get a ``failed. Received HTTP code 000`` message if there are problems-->

<!-- ## Generate Test Data

```bash
make generate
```

Generattes loads of test data, ctrl-c to exit -->

## API Testing with CURL

If you want to do more manual testing, here are the curl commands to use

### Test Health Endpoint

This endpoint supports the promethius monitoring standards for a healthcheck endpoint

```bash
curl http://localhost:8090/api/health/

```

### Test Config Endpoint

```bash
curl http://localhost:8090/api/config/

```

### Test get all encounters

```bash
curl http://localhost:8090/api/encounters/
```

### Test add a new encounter

```bash
curl -X POST http://localhost:8090/api/encounters/ \
     -d '{"personId":"aaaa00000000000000000000", "mentorId":"aaaa00000000000000000000"}'

```

### Test update an encounter

```bash
curl -X PATCH http://localhost:8090/api/encounters/aaaa00000000000000000021 \
     -d '{"planId":"aaaa00000000000000000000"}'

```

### Test get an encounter

```bash
curl http://localhost:8090/api/encounters/aaaa00000000000000000000

```

### Test get all plans

```bash
curl http://localhost:8090/api/plans/
```

### Test add a new plan

```bash
curl -X POST http://localhost:8090/api/plans/ \
     -d '{"personId":"aaaa00000000000000000000", "mentorId":"aaaa00000000000000000000"}'

```

### Test update a plan

```bash
curl -X PATCH http://localhost:8090/api/plans/aaaa00000000000000000021 \
     -d '{"planId":"aaaa00000000000000000000"}'

```

### Test get a plan

```bash
curl http://localhost:8090/api/plans/aaaa00000000000000000000

```

## Observability and Configuration

The ```api/config/``` endpoint will return a list of configuration values. These values are either "defaults" or loaded from an Environment Variable, or found in a singleton configuration file of the same name. Configuration files take precidence over environment variables. The variable "CONFIG_FOLDER" will change the location of configuration files from the default of ```./```

The ```api/health/``` endpoint is a Promethius Healthcheck endpoint.

The [Dockerfile](./Dockerfile) uses a 2-stage build, and supports both amd64 and arm64 architectures. See [docker-build.sh](./src/docker/docker-build.sh) for details about how to build in the local architecture for testing, and [docker-push.sh] for details about how to build and push multi-architecture images.
