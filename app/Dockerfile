# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry install --no-root

# Copy the project files into the container
COPY . /app/

# Expose the port that Django will run on
EXPOSE 8000
