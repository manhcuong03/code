from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from loginHandle import LOGIN_HANDLE
from mainHandle import MAIN_HANDLE
import cv2


class UI():
    def __init__(self):
        self.mainUI = QMainWindow()
        self.mainHandle = MAIN_HANDLE(self.mainUI)
        self.mainHandle.btnLogout.clicked.connect(lambda: self.loadLoginForm())
        self.loginUI = QMainWindow()
        self.loginHandle = LOGIN_HANDLE(self.loginUI)
        self.loginHandle.btnLogin.clicked.connect(lambda: self.loadMainForm(0))
        self.mainHandle.btnCam.clicked.connect(lambda: self.start_camera())
        self.loginUI.show()

        # Biến camera và timer
        self.cap = None
        self.timer = QTimer()

    def loadMainForm(self, data):
        self.loginUI.hide()
        self.mainUI.show()

    def loadLoginForm(self):
        self.mainUI.hide()
        self.loginUI.show()

    def start_camera(self):
        """Khởi động camera và bắt đầu hiển thị hình ảnh."""
        if not self.cap:
            self.cap = cv2.VideoCapture(0)  # Mở camera mặc định
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Cập nhật mỗi 30ms

    def update_frame(self):
        """Cập nhật hình ảnh từ camera lên QLabel."""
        ret, frame = self.cap.read()
        if ret:
            # Chuyển đổi hình ảnh từ BGR (OpenCV) sang RGB (Qt)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.mainHandle.lbl_img.setPixmap(pixmap)  # Hiển thị trên QLabel
            self.mainHandle.lbl_img.setScaledContents(True)  # Đảm bảo ảnh vừa khung

    def stop_camera(self):
        """Dừng camera khi không cần nữa."""
        if self.cap:
            self.timer.stop()
            self.cap.release()
            self.cap = None

    def __del__(self):
        """Hủy tài nguyên khi thoát chương trình."""
        self.stop_camera()


if __name__ == "__main__":
    app = QApplication([])

    ui = UI()

    app.exec_()
