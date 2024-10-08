import curses
import os
import subprocess

def check_terminal():
    # Проверка наличия gnome-terminal
    result = subprocess.run(['which', 'gnome-terminal'], stdout=subprocess.PIPE)
    if result.returncode == 0:
        return 'gnome-terminal'
    
    # Проверка наличия xfce4-terminal
    result = subprocess.run(['which', 'xfce4-terminal'], stdout=subprocess.PIPE)
    if result.returncode == 0:
        return 'xfce4-terminal'
    
    return None

def main(stdscr):
    # Инициализация curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Получаем размеры окна
    sh, sw = stdscr.getmaxyx()

    # Создаем окно для вывода текста
    win = curses.newwin(sh - 3, sw, 0, 0)
    win.border(0)

    # Создаем окно для ввода команд
    cmd_win = curses.newwin(3, sw, sh - 3, 0)
    cmd_win.border(0)
    cmd_win.addstr(1, 1, "Command: ")

    # Проверка наличия терминала
    terminal = check_terminal()
    if terminal is None:
        win.addstr(1, 1, "No supported terminal found (gnome-terminal or xfce4-terminal).")
        win.refresh()
        cmd_win.refresh()
        stdscr.getch()
        return

    # Основной цикл
    while True:
        # Обновляем окна
        win.refresh()
        cmd_win.refresh()

        # Получаем команду от пользователя
        cmd_win.addstr(1, 10, " " * (sw - 12))
        cmd_win.refresh()
        cmd = cmd_win.getstr(1, 10, sw - 12).decode('utf-8')

        # Выполняем команду
        if cmd == "exit":
            break
        elif cmd.startswith("edit "):
            filename = cmd.split(" ")[1]
            os.system(f"vim {filename}")
        elif cmd.startswith("run "):
            filename = cmd.split(" ")[1]
            os.system(f"{terminal} -- bash -c 'python3 {filename}; exec bash'")
        else:
            win.addstr(1, 1, f"Unknown command: {cmd}")

if __name__ == "__main__":
    curses.wrapper(main)
