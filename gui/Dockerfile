#=========================================================================================
# Docker-образ с полным набором средств разработки на базе Linux,
# включая утилиты, IDE, SDK, языки программирования и библиотеки,
# а также графическую среду XFCE4.
# Это позволит иметь готовую среду разработки,
# которую можно легко развернуть на любом сервере, поддерживающем Docker.
#
# Порядок создания Docker-образа:
#  Создать Dockerfile: В этом файле будут описаны все шаги для создания вашего образа.
#  Установить необходимые пакеты и утилиты: все необходимые инструменты и библиотеки.
#  Установить XFCE4 и VNC сервер: позволит вам подключаться к графической среде через VNC.
#=========================================================================================

# Используем базовый образ Ubuntu
FROM ubuntu:20.04

# Устанавливаем временную зону по умолчанию и отключаем интерактивный режим
ENV DEBIAN_FRONTEND=noninteractive

# Обновляем пакеты и устанавливаем необходимые утилиты, включая tzdata
RUN apt-get update && apt-get install -y \
    tzdata \
    sudo \
    wget \
    curl \
    git \
    vim \
    xfce4 \
    xfce4-goodies \
    xorg \
    dbus-x11 \
    x11-xserver-utils \
    novnc \
    websockify \
    supervisor \
    xfce4-terminal \
    firefox \
    terminator \
    mc \
    python3 \
    python3-pip \
    nodejs \
    npm \
    golang \
    ruby \
    vagrant \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Настраиваем временную зону
RUN ln -fs /usr/share/zoneinfo/Europe/Kiev /etc/localtime && \
    echo "Europe/Kiev" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Устанавливаем Docker и Docker Compose
RUN curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh && rm get-docker.sh
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

# Устанавливаем VNC сервер
RUN apt-get update && apt-get install -y \
    tightvncserver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем VSCode
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg \
    && install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/ \
    && sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list' \
    && apt-get install apt-transport-https \
    && apt-get update \
    && apt-get install -y code

# Устанавливаем Flask
RUN pip3 install flask

# Создаем пользователя devel для работы
RUN useradd -m devel && echo "devel:devel" | chpasswd && adduser devel sudo

# Копируем конфигурационные файлы
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY xstartup /home/devel/.vnc/xstartup

# Изменяем права доступа к файлу xstartup от имени пользователя root
RUN chmod +x /home/devel/.vnc/xstartup

# Настраиваем VNC сервер от имени пользователя root
RUN mkdir -p /home/devel/.vnc
RUN echo "devel" | vncpasswd -f > /home/devel/.vnc/passwd
RUN chmod 600 /home/devel/.vnc/passwd

# Создаем директорию для логов Supervisor и устанавливаем права доступа
RUN mkdir -p /var/log/supervisor
RUN chown -R devel:devel /var/log/supervisor

# Устанавливаем переменную окружения USER для пользователя devel
ENV USER=devel

# Переключаемся на пользователя devel
USER devel

# Открываем порты для VNC и noVNC
EXPOSE 5901
EXPOSE 6080

# Переключаемся обратно на пользователя root для запуска Supervisor
USER root
    
# Запускаем Supervisor для управления процессами
CMD ["/usr/bin/supervisord"]
