# Use an official Python runtime as a parent image
FROM python:3.8

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

# Copy project
COPY . /app/

# Start uWSGI
CMD ["uwsgi", "--http", ":8888", "--module", "maya.wsgi:application"]