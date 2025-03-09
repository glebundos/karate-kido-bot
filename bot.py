import pyautogui
import mss  # Использование mss для захвата экрана
import numpy as np
import time
import keyboard  # Библиотека для отслеживания клавиш
#import cv2
#import pytesseract
from datetime import datetime
import pygetwindow as gw
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Координаты областей для захвата (замени на свои)
left_area = (148, 336, 149, 337)   # (x1, y1, x2, y2)
right_area = (230, 336, 231, 337)  # (x1, y1, x2, y2)
# score_area = (155, 82, 211, 102)

# Координаты кликов (замени на свои)
left_click = (148, 500)   # Координаты клика по левой области
right_click = (235, 500)  # Координаты клика по правой области

# Список цветов пикселей для проверки появления "ветки" (замени на нужные тебе цвета)
non_branch_colors = [(63, 156, 255, 255), (64, 156, 255, 255)]  # Пример цвета, который не является веткой
branch_colors = [(43, 39, 72, 255), (40, 77, 148, 255), (34, 60, 125, 255), (56, 54, 76, 255)]  # Пример цвета, который является веткой

def move_window(window_title, x, y):
    """Перемещает окно с указанным заголовком на новые координаты (x, y)."""
    try:
        window = gw.getWindowsWithTitle(window_title)[0]  # Получаем окно по заголовку
        window.moveTo(x, y)  # Перемещаем окно в указанные координаты
        print(f"Окно '{window_title}' перемещено в ({x}, {y})")
    except IndexError:
        print(f"Окно с заголовком '{window_title}' не найдено.")

# Функция для захвата области экрана с использованием mss (быстрее, чем pyscreenshot)
def capture_area(area):
    with mss.mss() as sct:
        # Указываем область захвата
        monitor = {"top": area[1], "left": area[0], "width": area[2] - area[0], "height": area[3] - area[1]}
        img = sct.grab(monitor)
        return np.array(img)  # Преобразование в массив numpy

# def read_number_from_screen(region):
#     """
#     Считывает цифры с экрана в заданной области.

#     :param region: Кортеж (left, top, width, height) с координатами области.
#     :return: Распознанная строка с цифрами.
#     """
#     with mss.mss() as sct:
#         screenshot = sct.grab(region)
#         img = np.array(screenshot)

#         # Преобразование в оттенки серого
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         # Бинаризация для улучшения OCR
#         _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

#         # Используем pytesseract для распознавания текста
#         custom_config = r'--oem 3 --psm 6 outputbase digits'
#         text = pytesseract.image_to_string(thresh, config=custom_config)

#         return text.strip()

# Функция для получения цвета пикселя
def get_pixel_color(area):
    img = capture_area(area)
    return tuple(img[0, 0])  # Получаем цвет пикселя в верхнем левом углу (0, 0)

# Функция для проверки, является ли цвет пикселя одним из заданных
def is_branch_color(color):
    return color in branch_colors

# Логирование цветов пикселей в консоль
def log_pixel_color(area, color):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - Координаты {area}: Цвет {color}")

# Инициализация
click_side = "left"  # Начальная сторона кликов: "left" или "right"
to_left_after = 0  # Счетчик кликов слева
to_right_after = 0  # Счетчик кликов справа
total_clicks = 0
break_score = 0
print("Бот запущен! Нажми 'B' для остановки.")

move_window("Mini App: Karate Kido", 0, 0)
# Основной цикл
try:
    while True:
        if keyboard.is_pressed('b'):  # Проверка нажатия клавиши 'B'
            print("Бот остановлен по нажатию клавиши 'B'.")
            break  # Выход из цикла, остановка бота

        time.sleep(0.02)

        # Получаем текущие цвета пикселей в обеих областях
        curr_left_color = get_pixel_color(left_area)
        curr_right_color = get_pixel_color(right_area)

        # Логируем текущие цвета пикселей в консоль
        # log_pixel_color(left_area, curr_left_color)
        # log_pixel_color(right_area, curr_right_color)

        # Логируем текущие цвета пикселей в консоль
        # log_pixel_color("left is branch: ", is_branch_color(curr_left_color))
        # log_pixel_color("right is branch: ",is_branch_color(curr_right_color))

        if is_branch_color(curr_left_color):
            to_right_after = 2
        elif is_branch_color(curr_right_color):
            to_left_after = 2


        if click_side == "left":
            pyautogui.click(left_click)
        else:
            pyautogui.click(right_click)

        total_clicks += 1

        to_left_after -= 1
        to_right_after -= 1

        if to_right_after == 0:
            click_side = "right"
        if to_left_after == 0:
            click_side = "left"

        # print(f"To left after {to_left_after}")
        # print(f"To right after {to_right_after}")

        # print("score: ", read_number_from_screen(score_area))

        if total_clicks == break_score and break_score > 0:
            break

except KeyboardInterrupt:
    print("\nБот остановлен.")
