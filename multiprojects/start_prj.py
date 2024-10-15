#!/usr/bin/env python3

"""
Для автоматизации процесса создания и выбора проектов в Docker-контейнере,
можно написать скрипт на Python, который будет выполнять следующие задачи:

Создавать структуру папок для нового проекта.
Предоставлять меню для выбора существующего проекта.
Открывать терминал, файловый менеджер и Visual Studio Code в папке проекта.
"""

import os
import subprocess
import sys

# Путь к общему каталогу для всех проектов python
BASE_DIR = os.path.expanduser("~/python_prj")

# Структура папок для каждого проекта
PROJECT_STRUCTURE = ["shared_folder", "app_folder", "data_folder"]

def create_project(project_name):
    """Создает структуру папок для нового проекта."""
    project_path = os.path.join(BASE_DIR, project_name)
    os.makedirs(project_path, exist_ok=True)
    for folder in PROJECT_STRUCTURE:
        os.makedirs(os.path.join(project_path, folder), exist_ok=True)
    print(f"Проект {project_name} создан.")

def list_projects():
    """Возвращает список всех проектов."""
    return [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]

def open_project(project_name):
    """Открывает терминал, файловый менеджер и VSCode в папке проекта."""
    project_path = os.path.join(BASE_DIR, project_name)
    if not os.path.exists(project_path):
        print(f"Проект {project_name} не существует.")
        return

    # Открыть новый терминал и перейти в папку проекта
    #subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'cd {project_path}; exec bash'])
    subprocess.Popen(['x-terminal-emulator', '-e', f'bash -c "cd {project_path}; exec bash"'])

    # Открыть файловый менеджер в папке проекта
    subprocess.Popen(['xdg-open', project_path])

    # Открыть VSCode в папке проекта
    subprocess.Popen(['code', project_path])

def main():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    projects = list_projects()
    print("Доступные проекты:")
    for i, project in enumerate(projects, start=1):
        print(f"{i}. {project}")
    print(f"{len(projects) + 1}. Создать новый проект")

    choice = input("Выберите проект для работы (введите номер): ")

    try:
        choice = int(choice)
    except ValueError:
        print("Некорректный ввод.")
        sys.exit(1)

    if choice == len(projects) + 1:
        new_project_name = input("Введите имя нового проекта: ")
        create_project(new_project_name)
        open_project(new_project_name)
    elif 1 <= choice <= len(projects):
        open_project(projects[choice - 1])
    else:
        print("Некорректный выбор.")

if __name__ == "__main__":
    main()

"""
start_prj.py

Комментарии к коду:
* BASE_DIR:          Указывает на общий каталог для всех проектов.
* PROJECT_STRUCTURE: Определяет структуру папок для каждого проекта.
* create_project:    Создает структуру папок для нового проекта.
* list_projects:     Возвращает список всех существующих проектов.
* open_project:      Открывает новый терминал, файловый менеджер и Visual Studio Code.
* main:              Основная функция, меню для выбора проекта или создания.

Запуск скрипта:
1. должны быть установлены gnome-terminal, xdg-open и Visual Studio Code.
2. Сохраните скрипт в файл, например, prj_manager.py.
3. Запустите скрипт с помощью Python:   python3 start_prj.py
"""