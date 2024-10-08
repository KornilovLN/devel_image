# Базовый образ
FROM ubuntu:22.04 as base_os

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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=noninteractive

# Установка Docker и утилит
FROM base_os as docker_utils

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu jammy stable" \
    && apt-get update \
    && apt-get install -y docker-ce \
    && useradd -m dockeruser && usermod -aG docker dockeruser \
    && curl -L "https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    && ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose \
    && docker-compose --version \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Go и необходимых инструментов
FROM docker_utils as go_dev

# Установка Go
RUN wget https://golang.org/dl/go1.21.5.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz \
    && rm go1.21.5.linux-amd64.tar.gz

ENV PATH=$PATH:/usr/local/go/bin
ENV GOPATH=/go
ENV PATH=$PATH:$GOPATH/bin

# Создание рабочей директории
WORKDIR /go/src/app

# Инициализация модуля Go
RUN go mod init myapp

# Установка Go инструментов
RUN go install golang.org/x/tools/gopls@v0.14.2 \
    && go install github.com/go-delve/delve/cmd/dlv@v1.22.0 \
    && go install github.com/fatih/gomodifytags@v1.16.0 \
    && go install github.com/josharian/impl@v1.2.0 \
    && go install github.com/cweill/gotests/gotests@v1.6.0 \
    && go install github.com/haya14busa/goplay/cmd/goplay@v1.0.0 \
    && go install github.com/go-swagger/go-swagger/cmd/swagger@v0.30.5

# Добавление зависимостей в go.mod
RUN go get github.com/gin-gonic/gin@v1.9.1 \
    && go get github.com/gorilla/mux@v1.8.1 \
    && go get github.com/labstack/echo/v4@v4.11.3

# Загрузка зависимостей
RUN go mod download

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libusb-1.0-0-dev \
    libbluetooth-dev \
    libmodbus-dev \
    build-essential \
    gdb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Добавление Go зависимостей
RUN go get github.com/tarm/serial@v0.0.0-20180830185346-98f6abe2eb07 \
    && go get github.com/google/gousb@v1.1.2 \
    && go get github.com/gorilla/websocket@v1.5.1 \
    && go get github.com/paypal/gatt@v0.0.0-20151011220935-4ae819d591cf \
    && go get github.com/goburrow/modbus@v0.1.0 \
    && go get periph.io/x/conn/v3@v3.7.0 \
    && go get periph.io/x/host/v3@v3.8.2

# Загрузка зависимостей
RUN go mod download

# Очистка кэша Go
RUN go clean -cache -modcache -i -r


FROM go_dev as go_bases

# Добавление MongoDB репозитория
RUN apt-get update && apt-get install -y gnupg wget software-properties-common \
    && wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add - \
    && echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Установка драйверов и инструментов для работы с базами данных
RUN apt-get update && apt-get install -y \
    postgresql-client \
    mongodb-org \
    sqlite3 \
    redis-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Добавление Go зависимостей для баз данных
RUN go get github.com/lib/pq@v1.10.9 \
    go.mongodb.org/mongo-driver/mongo@v1.13.1 \
    github.com/mattn/go-sqlite3@v1.14.19 \
    github.com/jackc/pgx/v4@v4.18.1 \
    github.com/go-sql-driver/mysql@v1.7.1 \
    github.com/influxdata/influxdb-client-go/v2@v2.13.0 \
    github.com/rethinkdb/rethinkdb-go@v4.0.0 \
    github.com/golang-migrate/migrate/v4@v4.17.0 \
    github.com/volatiletech/sqlboiler/v4@v4.15.0 \
    github.com/volatiletech/sqlboiler/v4/drivers/sqlboiler-psql@v4.15.0 \
    github.com/volatiletech/sqlboiler/v4/drivers/sqlboiler-mysql@v4.15.0 \
    github.com/volatiletech/sqlboiler/v4/drivers/sqlboiler-sqlite3@v4.15.0 \
    gorm.io/gorm@v1.25.5 \
    gorm.io/driver/postgres@v1.5.4 \
    gorm.io/driver/mysql@v1.5.2 \
    gorm.io/driver/sqlite@v1.5.4 \
    github.com/go-redis/redis/v8@v8.11.5

# Загрузка зависимостей и очистка
RUN go mod tidy && go mod download && go clean -cache -modcache -i -r


# Настройка рабочей директории
WORKDIR /go/src/app

# Запуск bash при старте контейнера
CMD ["/bin/bash"]
