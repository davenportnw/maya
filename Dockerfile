# Use an official Python runtime as a parent image
FROM python:3.11


# Set environment variables using the ARG values
ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST

ENV POSTGRES_DB=${POSTGRES_DB}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_HOST=${POSTGRES_HOST}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Install uWSGI
RUN pip install uwsgi

# Install PostgreSQL development libraries
RUN apt-get update && apt-get install -y libpq-dev

# Copy project
COPY . /app/

# Start uWSGI
CMD ["uwsgi", "--http", ":8888", "--module", "maya.wsgi:application"]