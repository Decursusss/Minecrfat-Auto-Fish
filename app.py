import time
import keyboard
import cv2
import numpy as np
import mss
import pyautogui
import win32gui
import win32con
import pygetwindow as gw

lower_red1 = np.array([41, 41, 255])  # dlja rgba(208,41,41,255)
upper_red1 = np.array([135, 20, 20])  # dlja rgba(135,20,20,255)

lower_red2 = np.array([20, 20, 135])
upper_red2 = np.array([208, 41, 208])

lower_white = np.array([190, 190, 190])  # dlja rgba(143,143,143,255)
upper_white = np.array([208, 208, 208])  # dlja rgba(208,208,208,255)

# poplavok templates
poplavok_templates = [
    cv2.imread('poplavkiDay/poplavok1.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('poplavkiDay/poplavok2.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('poplavkiDay/poplavok3.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('poplavkiDay/poplavok4.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('poplavkiDay/poplavok5.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('poplavkiDay/poplavok6.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('poplavkiDay/poplavok7.png', cv2.IMREAD_GRAYSCALE),
]

#zahvativajem ekran
# def capture_screen():
#     with mss.mss() as sct:
#         monitor = sct.monitors[1]
#         img = np.array(sct.grab(monitor))[:, :, :3]
#         return img


def capture_screen():
    app_name = "Minecraft* 1.21.4 - Одиночная игра"
    windows = gw.getWindowsWithTitle(app_name)
    if not windows:
        print(f"Приложение с названием '{app_name}' не найдено!")
        return None

    hwnd = windows[0]._hWnd

    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

    rect = win32gui.GetWindowRect(hwnd)
    x, y, x1, y1 = rect
    width = x1 - x
    height = y1 - y

    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        img = np.array(sct.grab(monitor))[:, :, :3]
        return img


#nahodim sovpadenija po poplovku template esli nahodim peredajem koordinati dlja otrisovki
def find_bobber(frame, templates):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for poplavok_template in templates:
        result = cv2.matchTemplate(gray_frame, poplavok_template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.52
        locations = np.where(result >= threshold)

        for pt in zip(*locations[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + poplavok_template.shape[1], pt[1] + poplavok_template.shape[0]),
                          (0, 255, 0), 2)
            return pt

    return None

#sozdaem masku dlja zahvata
def apply_color_mask(frame):
    mask_red1 = cv2.inRange(frame, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(frame, lower_red2, upper_red2)
    mask_white = cv2.inRange(frame, lower_white, upper_white)

    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask = cv2.bitwise_or(mask_red, mask_white)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    return result

fishing_active = False

#vkluchits/vikluchits ribalku
def toggle_fishing():
    global fishing_active
    fishing_active = not fishing_active
    print("Авто-рыбалка ВКЛ 🟢" if fishing_active else "Авто-рыбалка ВЫКЛ 🔴")

keyboard.add_hotkey("F1", toggle_fishing)

counter = 0

while True:
    current_frame = capture_screen()

    masked_frame = apply_color_mask(current_frame)

    if fishing_active:
        bobber_position = find_bobber(masked_frame, poplavok_templates)

        if bobber_position:
            counter = 0
        else:
            counter -= 1

        if counter <= -3:
            pyautogui.rightClick()
            print("ПОЙМАЛ РЫБУ 🦈")
            counter = 0
            time.sleep(1)
            print("ЗАБРАСЫВАЮ ПОПЛОВОК 🎣")
            pyautogui.rightClick()
            time.sleep(2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break