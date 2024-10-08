## Допустим, необходимо иметь набор на основе:
1. Python3, pip3, flask, библиотек для python {numpy, pandas, matplot, QT, scipy, SQLite...} утилит типа {conda, jupyter notebook, jupyter lab, ...},
* то мы для работы собираем образ на базе, например, ubuntu2204,
* и затем разворачиваем контейнер с подключением к нему необходимых томов и общих папок и прочих настроек, для того, чтобы разрабатывать проект средствами контейнерных программ и библиотек, но наработки держать на хосте, либо где-то на VM, к которой есть доступ по ssh.
* И пусть контейнер сей называется python-factory.

2. Это одно, Но нам хочется построить аналогичную среду назработки на основе Rust и всей его инфраструктуры из библиотек, утилит, фреймворков,... И мы опять сооружаем такой контейнер из другого образа (например с названием rust_factory)

3. Наконец, есть сотрудник, владеющий GO средой программирования, а другой - на C++ пишет...

4. Тогда мы думаем. А почему бы нам не создать ряд фабрик по каждому направлению и не направить их на один и тот же проект (он в каком-то общем репозитории будет) 

5. Поскольку базис мы выберем как ubuntu 2204,  то тут можно сэкономить память за счет общих слоев.

6. В дополнение - создать yaml файл для генерации контейнеров с базами данных разных типов. Тогда из приложений можно будет достукиваться к необходимым БД.


### Создание Dockerfile для каждой "фабрики":

**_Python Factory: Dockerfile.python_**
```
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    flask \
    numpy \
    pandas \
    matplotlib \
    PyQt5 \
    scipy \
    jupyter \
    jupyterlab

WORKDIR /project

CMD ["bash"]
```
**_Rust Factory: Dockerfile.rust_**
```
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

RUN rustup component add rustfmt clippy

WORKDIR /project

CMD ["bash"]
```

**_Go Factory: Dockerfile.go_**
```
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    golang \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project

CMD ["bash"]
```

**_C++ Factory Dockerfile.cpp:_**
```
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gdb \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project

CMD ["bash"]
```

**_Docker Compose файл для баз данных: docker-compose.db.yml_**
```
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: example
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: example
    volumes:
      - mysql_data:/var/lib/mysql

  mongodb:
    image: mongo:4.4
    volumes:
      - mongodb_data:/data/db

volumes:
  postgres_data:
  mysql_data:
  mongodb_data:
```

**_Основной Docker Compose файл для запуска всех "фабрик": docker-compose.yml_**
```
version: '3.8'

services:
  python_factory:
    build:
      context: .
      dockerfile: Dockerfile.python
    volumes:
      - ./project:/project
    ports:
      - "8888:8888"  # для Jupyter

  rust_factory:
    build:
      context: .
      dockerfile: Dockerfile.rust
    volumes:
      - ./project:/project

  go_factory:
    build:
      context: .
      dockerfile: Dockerfile.go
    volumes:
      - ./project:/project

  cpp_factory:
    build:
      context: .
      dockerfile: Dockerfile.cpp
    volumes:
      - ./project:/project

networks:
  default:
    external:
      name: db_network
```

**_Запуск всего окружения: start_environment.sh_**
```
#!/bin/bash
docker network create db_network
docker-compose -f docker-compose.db.yml up -d
docker-compose up -d
```

**_Для запуска всего окружения выполните:_**
```
chmod +x start_environment.sh
./start_environment.sh
```

**_Этот подход позволяет:_**
* Использовать общий базовый образ Ubuntu 22.04 для экономии памяти.
* Изолировать среды разработки для разных языков.
* Хранить код проекта на хосте в папке ./project, которая монтируется во все контейнеры.
* Иметь доступ к различным базам данных из всех сред разработки.
* Разработчики могут подключаться к нужным им контейнерам через Docker exec или использовать их как удаленные среды разработки в своих IDE.

**_Для дополнительной настройки каждой "фабрики":_**
<br>вы можете добавить специфические инструменты и библиотеки в соответствующие Dockerfile.
<br>Например, для Rust можно добавить популярные крейты,
<br>для Go - часто используемые пакеты, и т.д.