FROM ubuntu:22.04 as base_os
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    sudo \
    tree \
    mc \
    terminator \
    vim \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
ENV DEBIAN_FRONTEND=noninteractive

#-----------------------------------
FROM base_os as docker_utils   

RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    software-properties-common \ 
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable" \
    && apt-get update \
    && apt-get install -y docker-ce

RUN useradd -m dockeruser && usermod -aG docker dockeruser


RUN curl -L "https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    && ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

RUN docker-compose --version

#-----------------------------------
FROM docker_utils as python_utils

# Install zlib development libraries
RUN apt-get update && apt-get install -y zlib1g-dev libjpeg-dev

# Install Python 3.12 and development tools
RUN apt-get update && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python3.12 python3.12-venv python3.12-dev build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pip for Python 3.12 and update pip and setuptools
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
RUN pip3 install --upgrade pip setuptools wheel numpy

# Copy requirements.txt and install Python packages
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# Set Python 3.12 as the default python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Install database drivers
RUN pip3 install \
    pymongo \
    questdb \
    rethinkdb \
    psycopg2-binary \
    sqlalchemy


#-----------------------------------
FROM python_utils as flask

# Установка Flask и связанных плагинов
RUN pip3 install --upgrade --force-reinstall --ignore-installed Flask \
    Flask-Bootstrap \
    Flask-WTF \
    Flask-SQLAlchemy \
    Flask-Migrate \
    Flask-Login \
    Flask-RESTful \
    Flask-CORS \
    Flask-Caching \
    Flask-DebugToolbar \
    Flask-Mail
 
    
# Set the working directory
WORKDIR /app/flask


# Копирование файлов Flask-приложения (если есть)
COPY ./flask_app /app/flask

# Открытие порта для Flask (по умолчанию 5000)
EXPOSE 5000

# Команда для запуска Flask-приложения
CMD ["flask", "run", "--host=0.0.0.0"]