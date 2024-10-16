#!/bin/bash

# Update package list and install essential tools
sudo apt-get update
sudo apt-get install -y \
    wget \
    curl \
    sudo \
    tree \
    mc \
    terminator \
    vim \
    nano \
    apt-transport-https \
    ca-certificates \
    software-properties-common \
    build-essential \
    zlib1g-dev \
    libjpeg-dev \
    git

# Install Python 3.12 and development tools
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.12 python3.12-venv python3.12-dev

# Install pip for Python 3.12 and update pip and setuptools
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.12
sudo pip3 install --upgrade pip setuptools wheel numpy

# Install database drivers
sudo pip3 install \
    pymongo \
    questdb \
    rethinkdb \
    psycopg2-binary \
    sqlalchemy

# Set Python 3.12 as the default python version
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Copy requirements.txt to /tmp and install Python packages
sudo cp ./requirements.txt /tmp/requirements.txt
sudo pip3 install -r /tmp/requirements.txt