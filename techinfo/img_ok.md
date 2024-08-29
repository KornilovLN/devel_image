## Некоторые популярные Docker-образы сред разработки

NAME                      DESCRIPTION                                     STARS     OFFICIAL

### Languages

- gcc                       The GNU Compiler Collection is a compiling s…   860       [OK]

- python                    Python is an interpreted, interactive, objec…   9770      [OK]    :3.9
- 
- node                      Node.js is a JavaScript-based platform for s…   13610     [OK]    :14
- nodered/node-red          Low-code programming for event-driven applic…   690  
- circleci/node             Node.js is a JavaScript-based platform for s…   132  

- openjdk                   Pre-release / non-production builds of OpenJ…   3946      [OK]

- golang                    Go (golang) is a general purpose, higher-lev…   4923      [OK]

- ruby                      Ruby is a dynamic, reflective, object-orient…   2341      [OK]    :2.7

- php                       While designed for web development, the PHP …   7589      [OK]

- rust                      Rust is a systems programming language focus…   1005      [OK]    :1.51

### Frameworks

* Flask
```
FROM python:3.9
RUN pip install flask
```

* Express
```
FROM node:14
RUN npm install express express-generator mongo-express mongo mongoose mongoose-paginate-v2 
```

django                    DEPRECATED; use "python" instead                1220      [OK]
<br>or:
```
FROM python:3.9
RUN pip install django
```

* Ruby on rails:
```
FROM ruby:2.7
RUN gem install rails
```

* Laravel:
```
FROM php:7.4
RUN apt-get update && apt-get install -y \
    libzip-dev \
    zip \
&& docker-php-ext-install zip
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN composer global require laravel/installer
```

### DB

* postgres                  The PostgreSQL object-relational database sy…   13709     [OK]    :13
* mysql                     MySQL is a widely used, open-source relation…   15326     [OK]    :8.0
* redis                     Redis is the world’s fastest data platform f…   12975     [OK]    :6
* mongo                     MongoDB document databases provide high avai…   10357     [OK]    :4.4  
* mongo-express             Web-based MongoDB admin interface, written w…   1463      [OK]
* opentsdb/opentsdb         Opensource Time Series Database                 18 
* openlink/virtuoso-opensource-7 OpenLink Virtuoso Open Source Editionv7.2, 12 

### CI/CD

* jenkins/jenkins:lts       The leading open source automation server       3973 

* gitlab/gitlab-runner      GitLab CI Multi Runner used to fetch and run…   951

### web

* nginx                     Official build of Nginx.                        20126     [OK]   