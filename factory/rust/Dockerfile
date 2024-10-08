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

# Установка Rust
FROM docker_utils as rust_dev

RUN apt-get update && apt-get install -y build-essential
RUN apt-get update && apt-get install -y pkg-config libssl-dev

# Create rustuser first
RUN useradd -m rustuser

# Install Rust for rustuser
USER rustuser
WORKDIR /home/rustuser

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/home/rustuser/.cargo/bin:${PATH}"
RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc

# Установка дополнительных инструментов для Rust
RUN rustup component add rustfmt clippy

RUN cargo install cargo-edit cargo-watch cargo-tarpaulin cargo-outdated
RUN cargo install cargo-expand cargo-tree cargo-audit cargo-udeps cargo-modules cargo-make

# Настройка рабочей директории
WORKDIR /rust/src/app

# Запуск bash при старте контейнера
CMD ["/bin/bash"]
