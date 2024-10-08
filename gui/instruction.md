### Сборка и запуск Docker-образа:

**_Сборка Docker-образа:_**
```
docker build -t devel-img .
```

**_Запуск контейнер:_**
```
docker run -d -p 5901:5901 -p 6080:6080 --name devel-cont devel-img
```

**_Подключитесь к VNC:_**
```
Используйте VNC клиент для подключения к localhost:5901.
Используйте браузер для подключения к noVNC через http://localhost:6080.
```