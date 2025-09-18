import cv2

img = cv2.imread('diff.png')

# Gaussian blur
gauss = cv2.GaussianBlur(img, (5,5), sigmaX=1.0)

# Median filter (good for salt & pepper noise)
median = cv2.medianBlur(img, ksize=5)

# Bilateral filter (preserves edges)
bilat = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

# Save or show
cv2.imwrite('gauss.png', gauss)
cv2.imwrite('median.png', median)
cv2.imwrite('bilat.png', bilat)
