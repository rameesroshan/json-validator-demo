# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install the requirements
COPY requirements.txt /
RUN pip install  --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Set the working directory and install the validator package
WORKDIR /jsonvalidator
ADD . /jsonvalidator
RUN pip install  .
