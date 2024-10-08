# Базовый образ
FROM ubuntu:22.04 as base_os

ENV DEBIAN_FRONTEND=noninteractive

# Установка базовых утилит
RUN apt-get update && apt-get install -y \
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
    git \
    gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Docker и утилит
FROM base_os as docker_utils

RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y docker-ce \
    && useradd -m dockeruser && usermod -aG docker dockeruser \
    && curl -L "https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    && ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose \
    && docker-compose --version \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Nodejs и необходимых инструментов
FROM docker_utils as node_dev

# Установка Node.js и npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && node --version && npm --version

# Установка глобальных npm пакетов
RUN npm install -g yarn typescript ts-node nodemon @angular/cli @vue/cli create-react-app express-generator nest-cli

# Установка дополнительных инструментов для разработки и баз данных
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    postgresql \
    postgresql-contrib \
    sqlite3 \
    redis-server \
    libcairo2-dev \
    libjpeg-dev \
    libpango1.0-dev \
    libgif-dev \
    librsvg2-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

    # Установка MongoDB
    RUN curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | gpg --dearmor -o /etc/apt/keyrings/mongodb.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/mongodb.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list \
    && apt-get update \
    && apt-get install -y mongodb-org \
    && mkdir -p /data/db \
    && chown -R mongodb:mongodb /data/db \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка RethinkDB (если необходимо)
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libcurl4-openssl-dev \
    && wget https://download.rethinkdb.com/repository/ubuntu-focal/pool/r/rethinkdb/rethinkdb_2.4.2~0focal_amd64.deb \
    && dpkg -i rethinkdb_2.4.2~0focal_amd64.deb || true \
    && apt-get install -f -y \
    && rm rethinkdb_2.4.2~0focal_amd64.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка дополнительных зависимостей
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libcurl4-openssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Установка npm пакетов для работы с графикой
RUN npm install -g canvas sharp

# Настройка рабочей директории
WORKDIR /app

# Создание пользователя node
RUN useradd -m -s /bin/bash node && \
    chown -R node:node /app

# Переключение на пользователя node
USER node

# Запуск bash при старте контейнера
CMD ["/bin/bash"]
