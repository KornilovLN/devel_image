# Многоэтапная сборка

## позволяет разделить процесс сборки на несколько этапов,
<br>каждый из которых может использовать разные базовые образы
<br>и выполнять разные задачи.
<br>Это позволяет уменьшить размер конечного образа и улучшить управляемость.

### Этап 1: Установка базовой системы
FROM ubuntu:20.04 as base

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    curl \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

### Этап 2: Установка основных драйверов и библиотек
FROM base as drivers

RUN apt-get update && apt-get install -y \
    xorg \
    dbus-x11 \
    x11-xserver-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

### Этап 3: Установка утилит
FROM drivers as utilities

RUN apt-get update && apt-get install -y \
    git \
    xfce4 \
    xfce4-goodies \
    novnc \
    websockify \
    supervisor \
    xfce4-terminal \
    firefox \
    terminator \
    mc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

### Этап 4: Установка дополнительных инструментов
FROM utilities as tools

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nodejs \
    npm \
    golang \
    ruby \
    vagrant \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

### Этап 5: Установка Docker и Docker Compose
FROM tools as final

RUN curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh && rm get-docker.sh
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

### Настраиваем временную зону (!!!)
RUN ln -fs /usr/share/zoneinfo/Europe/Kiev /etc/localtime && \
    echo "Europe/Kiev" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

### Устанавливаем VNC сервер
RUN apt-get update && apt-get install -y \
    tightvncserver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

### Устанавливаем VSCode
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg \
    && install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/ \
    && sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list' \
    && apt-get install apt-transport-https \
    && apt-get update \
    && apt-get install -y code

### Устанавливаем Flask
RUN pip3 install flask

### Создаем пользователя devel для работы
RUN useradd -m devel && echo "devel:devel" | chpasswd && adduser devel sudo

### Настраиваем VNC сервер
USER devel
RUN mkdir -p /home/devel/.vnc
RUN echo "devel" | vncpasswd -f > /home/devel/.vnc/passwd
RUN chmod 600 /home/devel/.vnc/passwd

### Копируем конфигурационные файлы
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY xstartup /home/devel/.vnc/xstartup
RUN chmod +x /home/devel/.vnc/xstartup

### Открываем порты для VNC и noVNC
EXPOSE 5901
EXPOSE 6080

### Запускаем Supervisor для управления процессами
CMD ["/usr/bin/supervisord"]

# ========================================================================

## Dockerfile Пример использования внешних скриптов
<br>Также можно использовать внешние скрипты для установки различных компонентов.
<br>Это позволяет вам поддерживать отдельные скрипты для каждой группы пакетов и включать их в Dockerfile.

**_Пример структуры файлов:_**
```
.
├── Dockerfile
├── scripts
│   ├── install_base.sh
│   ├── install_drivers.sh
│   ├── install_utilities.sh
│   ├── install_tools.sh
│   └── install_vscode.sh
```

**_Пример Dockerfile:_**
```
# Используем базовый образ Ubuntu
FROM ubuntu:20.04

# Копируем скрипты в контейнер
COPY scripts /scripts

# Устанавливаем временную зону по умолчанию и отключаем интерактивный режим
ENV DEBIAN_FRONTEND=noninteractive

# Выполняем скрипты для установки компонентов
RUN /scripts/install_base.sh
RUN /scripts/install_drivers.sh
RUN /scripts/install_utilities.sh
RUN /scripts/install_tools.sh
RUN /scripts/install_vscode.sh

# Настраиваем временную зону
RUN ln -fs /usr/share/zoneinfo/Europe/Kiev /etc/localtime && \
    echo "Europe/Kiev" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Создаем пользователя devel для работы
RUN useradd -m devel && echo "devel:devel" | chpasswd && adduser devel sudo

# Настраиваем VNC сервер
USER devel
RUN mkdir -p /home/devel/.vnc
RUN echo "devel" | vncpasswd -f > /home/devel/.vnc/passwd
RUN chmod 600 /home/devel/.vnc/passwd

# Копируем конфигурационные файлы
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY xstartup /home/devel/.vnc/xstartup
RUN chmod +x /home/devel/.vnc/xstartup

# Открываем порты для VNC и noVNC
EXPOSE 5901
EXPOSE 6080

# Запускаем Supervisor для управления процессами
CMD ["/usr/bin/supervisord"]
```

**_Dockerfile Пример скрипта install_base.sh:_**
```
#!/bin/bash
apt-get update && apt-get install -y \
    sudo \
    wget \
    curl \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

<br>Аналогично можно создать скрипты для других групп пакетов.
<br>Этот подход позволяет вам легко управлять установкой различных компонентов и поддерживать Dockerfile в чистоте и порядке.

```
# Используем базовый образ Ubuntu
FROM ubuntu:20.04

# Устанавливаем временную зону по умолчанию и отключаем интерактивный режим
ENV DEBIAN_FRONTEND=noninteractive

# Обновляем пакеты и устанавливаем необходимые утилиты
RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    curl \
    vim \
    xfce4 \
    xfce4-goodies \
    xorg \
    dbus-x11 \
    x11-xserver-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Настраиваем временную зону
RUN ln -fs /usr/share/zoneinfo/Europe/Kiev /etc/localtime && \
    echo "Europe/Kiev" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Создаем пользователя devel для работы
RUN useradd -m devel && echo "devel:devel" | chpasswd && adduser devel sudo

# Настраиваем VNC сервер (если требуется)
USER devel
RUN mkdir -p /home/devel/.vnc
RUN echo "devel" | vncpasswd -f > /home/devel/.vnc/passwd
RUN chmod 600 /home/devel/.vnc/passwd

# Копируем конфигурационные файлы (если имеются)
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY xstartup /home/devel/.vnc/xstartup
RUN chmod +x /home/devel/.vnc/xstartup

# Открываем порты для VNC и noVNC (если требуется)
EXPOSE 5901
EXPOSE 6080

# Запускаем Supervisor для управления процессами (если требуется)
CMD ["/usr/bin/supervisord"]
```

<br>Этот Dockerfile устанавливает только XFCE4 и необходимые утилиты.

- Вы можете собрать образ с помощью следующей команды:
```
docker build -t xfce4-only .
```

- Затем запустите контейнер с этим образом:
```
docker run -d -p 5901:5901 -p 6080:6080 --name xfce4-only-container xfce4-only
```

- Если вам нужен готовый образ с XFCE4, вы можете поискать его на Docker Hub:
```
docker search xfce4
```
<br>Это покажет вам список доступных образов, которые могут содержать XFCE4.


<br>Т.е., применяя метод разбивки сборки докерфайла на логически связанные части элементов, и также - заранее создав , например, только просто сервер, и сервер с xfce4 , или еще какой стартовый образ, можно сварганить разные варианты целевых платформ. Остается для оператора сделать простое меню выбора в sh или python файле, и он сам себе сгенерирует нужный ему набор средств для работы

<br>Оператор сможет выбрать нужный набор средств для работы через простое меню, написанное на sh или python.

#### Пример реализации
1. Создание базовых образов
<br>Dockerfile для базового сервера:
```
# Используем базовый образ Ubuntu
FROM ubuntu:20.04

# Устанавливаем временную зону по умолчанию и отключаем интерактивный режим
ENV DEBIAN_FRONTEND=noninteractive

# Обновляем пакеты и устанавливаем необходимые утилиты
RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    curl \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Настраиваем временную зону
RUN ln -fs /usr/share/zoneinfo/Europe/Kiev /etc/localtime && \
    echo "Europe/Kiev" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Создаем пользователя devel для работы
RUN useradd -m devel && echo "devel:devel" | chpasswd && adduser devel sudo
```

### base-server.Dockerfile
<br>Dockerfile для сервера с XFCE4:
```
# Используем базовый образ Ubuntu
FROM ubuntu:20.04

# Устанавливаем временную зону по умолчанию и отключаем интерактивный режим
ENV DEBIAN_FRONTEND=noninteractive

# Обновляем пакеты и устанавливаем необходимые утилиты
RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    curl \
    vim \
    xfce4 \
    xfce4-goodies \
    xorg \
    dbus-x11 \
    x11-xserver-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Настраиваем временную зону
RUN ln -fs /usr/share/zoneinfo/Europe/Kiev /etc/localtime && \
    echo "Europe/Kiev" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Создаем пользователя devel для работы
RUN useradd -m devel && echo "devel:devel" | chpasswd && adduser devel sudo
```

### server-with-xfce4.Dockerfile
2. Скрипт для выбора и сборки образа
```
#!/bin/bash

echo "Выберите базовый образ для сборки:"
echo "1. Базовый сервер"
echo "2. Сервер с XFCE4"
read -p "Введите номер выбора: " choice

case $choice in
    1)
        docker build -f base-server.Dockerfile -t base-server .
        ;;
    2)
        docker build -f server-with-xfce4.Dockerfile -t server-with-xfce4 .
        ;;
    *)
        echo "Неверный выбор"
        exit 1
        ;;
esac

echo "Базовый образ успешно собран."
```
<br>build.sh

<br>Скрипт на python:
```
import os

def main():
    print("Выберите базовый образ для сборки:")
    print("1. Базовый сервер")
    print("2. Сервер с XFCE4")
    choice = input("Введите номер выбора: ")

    if choice == '1':
        os.system("docker build -f base-server.Dockerfile -t base-server .")
    elif choice == '2':
        os.system("docker build -f server-with-xfce4.Dockerfile -t server-with-xfce4 .")
    else:
        print("Неверный выбор")
        exit(1)

    print("Базовый образ успешно собран.")

if __name__ == "__main__":
    main()
```
<br>build.py

### Использование
1. Создайте файлы base-server.Dockerfile и server-with-xfce4.Dockerfile с соответствующим содержимым.
2. Создайте скрипт build.sh или build.py.
3. Запустите скрипт:
```
Для sh: ./build.sh
Для python: python build.py
```

#### Этот подход позволяет оператору выбрать нужный базовый образ и собрать его с помощью простого меню. Вы можете расширить этот метод, добавив дополнительные этапы и параметры для более сложных конфигураций