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

# Установка C++ и необходимых библиотек, инструментов, драйверов баз данных и т.д.
FROM docker_utils as cpp_dev

# Добавление репозитория для современных версий GCC и Clang
RUN add-apt-repository ppa:ubuntu-toolchain-r/test \
    && wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - \
    && echo "deb http://apt.llvm.org/jammy/ llvm-toolchain-jammy main" >> /etc/apt/sources.list \
    && echo "deb-src http://apt.llvm.org/jammy/ llvm-toolchain-jammy main" >> /etc/apt/sources.list

# Установка компиляторов и инструментов
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    gdb \
    valgrind \
    gcc-11 g++-11 \
    gcc-12 g++-12 \
    clang-13 \
    clang-14 \
    clang-15 \
    lldb \
    libc++-dev \
    libc++abi-dev \
    libboost-all-dev \
    libssl-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка современных систем сборки
RUN apt-get update && apt-get install -y python3-pip \
    && pip3 install conan meson \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка драйверов баз данных
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libmysqlclient-dev \
    libsqlite3-dev \
    libmongoc-dev \
    libbson-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка дополнительных инструментов
RUN apt-get update && apt-get install -y \
    ccache \
    cppcheck \
    clang-tidy \
    clang-format \
    doxygen \
    graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Настройка альтернатив для компиляторов
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 110 \
    --slave /usr/bin/g++ g++ /usr/bin/g++-11 \
    --slave /usr/bin/gcov gcov /usr/bin/gcov-11 \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 120 \
    --slave /usr/bin/g++ g++ /usr/bin/g++-12 \
    --slave /usr/bin/gcov gcov /usr/bin/gcov-12 \
    && update-alternatives --install /usr/bin/clang clang /usr/bin/clang-13 130 \
    --slave /usr/bin/clang++ clang++ /usr/bin/clang++-13 \
    && update-alternatives --install /usr/bin/clang clang /usr/bin/clang-14 140 \
    --slave /usr/bin/clang++ clang++ /usr/bin/clang++-14 \
    && update-alternatives --install /usr/bin/clang clang /usr/bin/clang-15 150 \
    --slave /usr/bin/clang++ clang++ /usr/bin/clang++-15

# Настройка рабочей директории
WORKDIR /workspace

# Создание пользователя developer
RUN useradd -m -s /bin/bash developer && \
    chown -R developer:developer /workspace

# Переключение на пользователя developer
USER developer

# Запуск bash при старте контейнера
CMD ["/bin/bash"]