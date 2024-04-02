# base stage
FROM python:3.12.2-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends  \
    gcc  \
    libpq-dev  \
    libgdal-dev

# Set the working directory
WORKDIR /app/

# Copy your project's configuration files
COPY requirements.txt /

# Install Python dependencies using Poetry
RUN pip install -r /requirements.txt

# build stage
FROM base AS build

RUN mkdir -p static

WORKDIR /app/

COPY ./startup.sh /startup
RUN sed -i 's/\r$//g' /startup

RUN chmod +x /startup

ADD ./src/. /app/
