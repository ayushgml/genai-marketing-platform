# Use the official Python image as a base image
FROM python:3.12-slim
 
# Install system dependencies required for building Python packages
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
 
# Install AWS CLI
RUN pip install --no-cache-dir awscli
 
# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the requirements file and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the application code and .env file into the container
COPY . .
 
# Expose port 5000 to the outside world
EXPOSE 5000
 
# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]