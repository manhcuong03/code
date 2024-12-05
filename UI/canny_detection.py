import cv2
import matplotlib.pyplot as plt

# Đọc ảnh đầu vào
image = cv2.imread("pcb1.jpg", cv2.IMREAD_GRAYSCALE)

# Làm mịn ảnh bằng GaussianBlur
blurred_image = cv2.GaussianBlur(image, (5, 5), 1.4)

# Áp dụng Canny Edge Detection
low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blurred_image, low_threshold, high_threshold)

# Hiển thị kết quả
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.title("Ảnh gốc")
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Ảnh phát hiện cạnh")
plt.imshow(edges, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
