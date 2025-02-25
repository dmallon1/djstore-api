# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7-alpine

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /djstore-api

# Set the working directory to /timesheets
WORKDIR /djstore-api

# Copy the current directory contents into the container at /timesheets
ADD . /djstore-api/

# RUN apt-get update
# RUN apt-get -y upgrade
# RUN apt-get install -y python3-pip

# RUN apt-get install -y nodejs
# RUN apt-get install -y npm

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
