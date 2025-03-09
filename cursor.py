import time
import sys
import mss
import numpy as np
import ctypes
import keyboard  # Импортируем библиотеку для отслеживания клавиш
import pygetwindow as gw

def move_window(window_title, x, y):
    """Перемещает окно с указанным заголовком на новые координаты (x, y)."""
    try:
        window = gw.getWindowsWithTitle(window_title)[0]  # Получаем окно по заголовку
        window.moveTo(x, y)  # Перемещаем окно в указанные координаты
        print(f"Окно '{window_title}' перемещено в ({x}, {y})")
    except IndexError:
        print(f"Окно с заголовком '{window_title}' не найдено.")

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_cursor_position():
    """Возвращает текущие координаты курсора."""
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def move_cursor(x, y):
    """Перемещает курсор на новые координаты."""
    ctypes.windll.user32.SetCursorPos(x, y)

def track_cursor():
    """Отслеживает положение курсора и выводит координаты в реальном времени. Добавлено управление стрелками для перемещения курсора."""
    print("Перемещайте курсор с помощью стрелок на клавиатуре. Нажмите Ctrl+C для выхода.\n")
    try:
        # move_window("Mini App: Karate Kido", 0, 0)
        move_cursor(435, 336)
        x, y = get_cursor_position()
        while True:
            # Проверяем нажатие стрелок
            if keyboard.is_pressed('up'):
                y -= 1
                # time.sleep(0.1)  # Делаем паузу, чтобы избежать слишком быстрого перемещения
            elif keyboard.is_pressed('down'):
                y += 1
                # time.sleep(0.1)
            elif keyboard.is_pressed('left'):
                x -= 1
                # time.sleep(0.1)
            elif keyboard.is_pressed('right'):
                x += 1
                # time.sleep(0.1)
            
            # Обновляем позицию курсора
            move_cursor(x, y)
            
            # Отображаем текущие координаты и цвет пикселя
            area = (x, y, x + 1, y + 1)
            color = get_pixel_color(area)
            sys.stdout.write(f"\rКоординаты: X={x:4}, Y={y:4}  Цвет пикселя: RGB{color}  ")
            sys.stdout.flush()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")

def get_pixel_color(area):
    img = capture_area(area)
    return tuple(img[0, 0])  # Получаем RGB цвет пикселя

def capture_area(area):
    with mss.mss() as sct:
        # Указываем область захвата
        monitor = {"top": area[1], "left": area[0], "width": area[2] - area[0], "height": area[3] - area[1]}
        img = sct.grab(monitor)
        return np.array(img)  # Возвращаем изображение как массив NumPy

if __name__ == "__main__":
    track_cursor()

# WEB VERSION
# ИГРАТЬ X= 435, Y= 620 
# СМОТРЕТЬ РЕКЛАМУ 455 380
# НЕСМОТРЕТЬ РЕКЛАМУ 455 450