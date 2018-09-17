import cv2
import numpy as np
from matplotlib import pyplot as plt

frame = cv2.imread('image.jpg',0)

#laplacian
laplacian = cv2.Laplacian(frame,cv2.CV_64F)

# 1.0 sobel
sobel = cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=5)

plt.subplot(2,2,1),plt.imshow(frame, cmap = 'gray')
plt.title('Orjinal'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(laplacian, cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobel, cmap = 'gray')
plt.title('Sobel'), plt.xticks([]), plt.yticks([])

plt.show()