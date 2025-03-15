# https://imagecolorpicker.com/ для выбора цветов
# SCRIPT dlja togo shtobi podobrats masku po screenshotam
import cv2
import numpy as np

image = cv2.imread('poplavkiDay/poplavok3.png')

lower_red1 = np.array([41, 41, 208])  # для rgba(208,41,41,255)
upper_red1 = np.array([135, 20, 20])  # для rgba(135,20,20,255)

lower_red2 = np.array([20, 20, 135])
upper_red2 = np.array([41, 41, 208])

lower_white = np.array([143, 143, 143])  # для rgba(143,143,143,255)
upper_white = np.array([208, 208, 208])  # для rgba(208,208,208,255)

mask_red1 = cv2.inRange(image, lower_red1, upper_red1)
mask_red2 = cv2.inRange(image, lower_red2, upper_red2)

mask_red = cv2.bitwise_or(mask_red1, mask_red2)

mask_white = cv2.inRange(image, lower_white, upper_white)

mask = cv2.bitwise_or(mask_red, mask_white)

result = cv2.bitwise_and(image, image, mask=mask)

cv2.imshow('Detected Bobber', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
