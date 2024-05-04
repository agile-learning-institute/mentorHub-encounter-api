# Base build stage
FROM python:3.10 AS base
  
WORKDIR /src
COPY . .

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Configure Pipenv & install depencies
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && \
    export PIPENV_VENV_IN_PROJECT=true && \
    pipenv install

# Copy server script & Bundle API as an executable
RUN pipenv run pyinstaller ./src/app/wsgi.py --onefile --name entrypoint

# Get branch and patch level, then create PATCH_LEVEL file
RUN BRANCH=$(git rev-parse --abbrev-ref HEAD) && \
    DATE=$(date "+%Y-%m-%d:%H:%M:%S") && \
    echo $DATE.$BRANCH > /src/PATCH_LEVEL

# Final stage
FROM ubuntu:latest AS deploy

WORKDIR /app

COPY --from=base /src/dist/entrypoint /app/entrypoint
COPY --from=base /src/PATCH_LEVEL /app/PATCH_LEVEL

# Install necessary packages or dependencies
RUN apt-get update -y && apt-get install gunicorn -y

EXPOSE 8090

CMD [ "./entrypoint" ]
