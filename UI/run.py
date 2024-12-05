from PyQt5.QtWidgets import QApplication, QMainWindow
from loginHandle import LOGIN_HANDLE
from mainHandle import MAIN_HANDLE
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import cv2
import time
class UI():
    def __init__(self):
        self.mainUI = QMainWindow()
        self.mainHandle = MAIN_HANDLE(self.mainUI)
        self.mainHandle.btnLogout.clicked.connect(lambda: self.loadLoginForm())
        self.loginUI = QMainWindow()
        self.loginHandle = LOGIN_HANDLE(self.loginUI)
        self.loginHandle.btnLogin.clicked.connect(lambda: self.loadMainForm(0))
        self.loginUI.show()
        
        # Date and time -----------------------------------------
        self.mainHandle.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.timer = QTimer(self.mainUI)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # Cập nhật mỗi giây
        # Date and time -----------------------------------------
        
        # Biến camera và timer-----------------------------------
        self.cap = None
        self.timer = QTimer()
        self.mainHandle.btnCapture.clicked.connect(lambda: self.capture_image())
        # Bảng giá trị -------------------------------------------
        self.mainHandle.table_result.setItem(0, 0, QtWidgets.QTableWidgetItem("STT"))
        self.mainHandle.table_result.setItem(0, 1, QtWidgets.QTableWidgetItem("Capacitor"))
        self.mainHandle.table_result.setItem(0, 2, QtWidgets.QTableWidgetItem("IC"))

            # Căn giữa tiêu đề cột
        self.mainHandle.table_result.item(0, 0).setTextAlignment(Qt.AlignCenter)
        self.mainHandle.table_result.item(0, 1).setTextAlignment(Qt.AlignCenter)
        self.mainHandle.table_result.item(0, 2).setTextAlignment(Qt.AlignCenter)
        # Bảng giá trị -------------------------------------------

    def loadMainForm(self, data):
        self.loginUI.hide()
        self.mainUI.show()
        self.start_camera()
    def loadLoginForm(self):
        self.mainUI.hide()
        self.loginUI.show()
        self.stop_camera()
    def update_datetime(self):
        """Cập nhật ngày giờ trên QDateTimeEdit."""
        current_datetime = QDateTime.currentDateTime()
        self.mainHandle.dateTimeEdit.setDateTime(current_datetime)
    # camera ---------------------------------------------------
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

    # camera --------------------------------------------------------------------------------------

    def capture_image(self):
        """Chụp ảnh từ camera và lưu vào file."""
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.captured_image = frame  # Lưu hình ảnh BGR từ OpenCV
                print("Ảnh đã được chụp và lưu vào biến `captured_image`.")

                # Tạo tên file với timestamp
                timestamp = time.strftime("%Y%m%d_%H%M%S")  # Ví dụ: 20241205_152030
                file_path = rf'D:\code\Final_xla\UI\img_capture\captured_image_{timestamp}.jpg'
                
                # Lưu ảnh
                cv2.imwrite(file_path, self.captured_image)
                print(f"Ảnh đã được lưu tại: {file_path}")

if __name__ == "__main__":
    app = QApplication([])
    
    ui = UI()

    app.exec_()