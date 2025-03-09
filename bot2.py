import pyautogui
import mss  
import numpy as np
import time
import keyboard 
from datetime import datetime
import pygetwindow as gw

left_area = (375, 336, 376, 337)   
right_area = (435, 336, 436, 337)  

left_click = (375, 500)   
right_click = (435, 500)  

non_branch_colors = [(63, 156, 255, 255), (64, 156, 255, 255)]  
branch_colors = [(22, 20, 70, 255), (23, 23, 75, 255), (25, 27, 80, 255), (56, 54, 76, 255)] 

def move_window(window_title, x, y):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]  
        window.moveTo(x, y)  
        print(f"Окно '{window_title}' перемещено в ({x}, {y})")
    except IndexError:
        print(f"Окно с заголовком '{window_title}' не найдено.")

def capture_area(area):
    with mss.mss() as sct:
        monitor = {"top": area[1], "left": area[0], "width": area[2] - area[0], "height": area[3] - area[1]}
        img = sct.grab(monitor)
        return np.array(img) 

def get_pixel_color(area):
    img = capture_area(area)
    return tuple(img[0, 0])

def is_branch_color(color):
    return color[2] < 200

def is_game_over(color1, color2):
    return color1[0] == color2[0]


def log_pixel_color(area, color):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - Координаты {area}: Цвет {color}")

def main():
    click_side = "left" 
    to_left_after = 0 
    to_right_after = 0
    total_clicks = 0
    break_score = 0
    autorestart = True

    print("Бот запущен! Нажми 'B' для остановки.")

    move_window("Play games, WIN REAL REWARDS! | GAMEE - Google Chrome", 0, 0)

    try:
        if click_side == "left":
            keyboard.press_and_release("left")
        else:
            keyboard.press_and_release("right") 
        
        while True:
            if keyboard.is_pressed('b'): 
                autorestart = False
                print("Бот остановлен по нажатию клавиши 'B'.")
                break 


            # time.sleep(0.012)

            curr_left_color = get_pixel_color(left_area)
            curr_right_color = get_pixel_color(right_area)

            if (total_clicks == break_score and break_score > 0) or is_game_over(curr_left_color, curr_right_color):
                break

            # Логируем текущие цвета пикселей в консоль
            # log_pixel_color(left_area, curr_left_color)
            # log_pixel_color(right_area, curr_right_color)

            # Логируем текущие цвета пикселей в консоль
            # log_pixel_color("left is branch: ", is_branch_color(curr_left_color))
            # log_pixel_color("right is branch: ",is_branch_color(curr_right_color))

            if is_branch_color(curr_left_color):
                to_right_after = 3
            elif is_branch_color(curr_right_color):
                to_left_after = 3
            elif is_branch_color(curr_left_color) and is_branch_color(curr_right_color):
                break

            if click_side == "left":
                keyboard.press_and_release("left")
            else:
                keyboard.press_and_release("right") 

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

        if autorestart:
            time.sleep(2)
            pyautogui.click(455, 450)
            time.sleep(2)
            pyautogui.click(455, 620)
            main()


    except KeyboardInterrupt:
        print("\nБот остановлен.")


if __name__ == "__main__":
    main()