import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('mevlana.png',0)
edges = cv2.Canny(img,50,150)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Orjinal'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Canny'), plt.xticks([]), plt.yticks([])

plt.show()