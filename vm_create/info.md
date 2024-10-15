## Создание на виртуальной машине сервера MongoDB средствами Ansible

0. Предполагается, что на виртуальной машине уже установлен docker и docker-compose. Иначе, см. файл docker_setup.sh
```
#!/bin/bash

echo "--- Installing Docker --------------------------------------------------------------"
sudo apt update
echo "------------------------------------------------------------------------------------"

echo "--- Installing utils --------------------------------------------------------------"
sudo apt install apt-transport-https ca-certificates curl software-properties-common
echo "------------------------------------------------------------------------------------"

echo "--- Добавьте ключ GPG для официального репозитория Docker в систему ----------------"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
echo "------------------------------------------------------------------------------------"

echo "--- Добавьте репозиторий Docker в источники APT ------------------------------------"
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
echo "------------------------------------------------------------------------------------"

echo "--- Обновите БД пакетов и добавьте Docker из недавно добавленного репозитория ------"
sudo apt update
echo "------------------------------------------------------------------------------------"

echo "--- Убедитесь, что установка будет выполняться из репозитория Docker ---------------"
apt-cache policy docker-ce
echo "------------------------------------------------------------------------------------"

echo "--- Установить Docker --------------------------------------------------------------"
sudo apt install docker-ce
echo "------------------------------------------------------------------------------------"

echo "--- Docker установлен, демон запущен, активирован запуск при загрузке --------------"
sudo systemctl status docker
echo "------------------------------------------------------------------------------------"

echo "--- Без sudo при запуске docker, добавьте свое имя пользователя в группу docker ----"
sudo usermod -aG docker ${USER}
echo "------------------------------------------------------------------------------------"

echo "--- Чтобы примен. добавление нового члена группы, выйд. и войдите на сервер или ----"
su - ${USER}
echo "------------------------------------------------------------------------------------"

echo "--- Проверьте, что ваш пользователь добавлен в группу docker, введя следующее ------"
id -nG
echo "------------------------------------------------------------------------------------"

echo "--- Если нужно доб. польз. в группу docker, объявите имя пользователя явно ---------"
sudo usermod -aG docker username
echo "------------------------------------------------------------------------------------"

echo "--- Установка Docker Compose -------------------------------------------------------"
sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose  
echo "------------------------------------------------------------------------------------"

echo "--- Версия Docker Compose ----------------------------------------------------------"
docker-compose --version
echo "------------------------------------------------------------------------------------"  
```

1. Непременное условие: Следует создать файл set_sshpass.sh для активации sshpass.
```
#!/bin/bash

echo "--- Установка sshpass --------------------------------------------------------------"
sudo apt update &&sudo apt install sshpass
echo "--
```
 
2. Создать файл inventory.yml для подключения к удаленному серверу на 192.168.88.101
```
[mongodb]
192.168.88.101 ansible_user=starmark ansible_password=!18leon28 ansible_become=yes ansible_become_method=sudo ansible_become_password=!18leon28

```

3. Создать файл install_mongo_docker.yml для установки MongoDB
```
---
- name: Install MongoDB Docker Container
  hosts: mongodb
  become: yes
  tasks:
    - name: Ensure Docker is installed
      apt:
        name: docker.io
        state: present
        update_cache: yes

    - name: Ensure Docker is started
      systemd:
        name: docker
        state: started
        enabled: yes

    - name: Create Docker network
      docker_network:
        name: net_mongo
        driver: bridge

    - name: Pull MongoDB Docker image
      docker_image:
        name: mongo
        tag: "5.0"
        source: pull

    - name: Run MongoDB container
      docker_container:
        name: mongodb
        image: mongo:5.0
        state: started
        restart_policy: always
        ports:
          - "27017:27017"
        networks:
          - name: net_mongo
        volumes:
          - /data/db:/data/db

    - name: Wait for MongoDB to start
      wait_for:
        host: "localhost"
        port: 27017
        delay: 10
        timeout: 300
```

4. Создать и запустить скрипт create_mongo_on_vm.yml
```
#!/bin/bash

ansible-playbook -i inventory.ini install_mongo_docker.yml
```
