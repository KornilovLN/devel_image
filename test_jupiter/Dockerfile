FROM jupyter/datascience-notebook

# Установка Flask
RUN pip install flask

# Копирование кода приложения
COPY app.py /app/
COPY templates/ /app/templates/

# Установка рабочей директории
WORKDIR /app

# Запуск приложения Flask
CMD ["python", "app.py"]