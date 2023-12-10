# Pull base image
FROM python:alpine3.17

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements/ ./requirements/
RUN pip install -r /code/requirements/production.txt

# Copy project
COPY . .
