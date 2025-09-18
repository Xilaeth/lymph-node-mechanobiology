import cv2

# Load image
img = cv2.imread('diff.png')

# Denoise color image
dst = cv2.fastNlMeansDenoisingColored(img, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21)

cv2.imwrite('denoised.png', dst)
