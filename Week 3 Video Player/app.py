import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QFileDialog, QComboBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
import cv2

class VideoPlayer(QMainWindow):
    mode = "normal"

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.video_path = ""
        self.cap = None
        self.frame_rate = 24
        self.total_frames = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.control_layout = QHBoxLayout()
        self.layout.addLayout(self.control_layout)

        self.open_button = QPushButton("Open Video")
        self.open_button.clicked.connect(self.open_video_file)
        self.control_layout.addWidget(self.open_button)

        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.clicked.connect(self.play_pause_video)
        self.control_layout.addWidget(self.play_pause_button)

        self.skip_backward_button = QPushButton("<<")
        self.skip_backward_button.clicked.connect(self.skip_backward)
        self.control_layout.addWidget(self.skip_backward_button)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)
        self.control_layout.addWidget(self.slider)

        self.skip_forward_button = QPushButton(">>")
        self.skip_forward_button.clicked.connect(self.skip_forward)
        self.control_layout.addWidget(self.skip_forward_button)

        self.speed_label = QLabel("Speed:")
        self.control_layout.addWidget(self.speed_label)

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.25x", "0.5x", "1x", "1.5x", "2x"])
        self.speed_combo.setCurrentIndex(2)  # Default speed is 1x
        self.speed_combo.currentIndexChanged.connect(self.set_speed)
        self.control_layout.addWidget(self.speed_combo)

        self.bw_button = QPushButton("Black & White")
        self.bw_button.clicked.connect(self.apply_bw_filter)
        self.control_layout.addWidget(self.bw_button)

    def open_video_file(self):
        file_dialog = QFileDialog()
        self.video_path, _ = file_dialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi)")
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.frame_rate = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.slider.setMaximum(self.total_frames)
            self.timer.start(1000 // self.frame_rate)

    def play_pause_video(self):
        if not self.timer.isActive():
            self.play_pause_button.setText("Pause")
            self.timer.start(1000 // self.frame_rate)
        else:
            self.play_pause_button.setText("Play")
            self.timer.stop()

    def update_frame(self): 
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # black and white filter
            if self.mode == "bw":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            h, w, _ = frame.shape
            img = QImage(frame.data, w, h, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.label.setPixmap(pixmap)
            self.slider.setValue(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
        else:
            self.timer.stop()
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.play_pause_button.setText("Play")

    def set_position(self, position):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)

    def skip_backward(self):
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        new_frame = max(0, current_frame - self.frame_rate)  # Skip 1 second backward
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)

    def skip_forward(self):
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        new_frame = min(self.total_frames, current_frame + self.frame_rate)  # Skip 1 second forward
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)

    def set_speed(self, index):
        speeds = {"0.25x": 0.25, "0.5x": 0.5, "1x": 1.0, "1.5x": 1.5, "2x": 2.0}
        speed = speeds[self.speed_combo.currentText()]
        self.frame_rate = int(self.cap.get(cv2.CAP_PROP_FPS) * speed)
        if self.timer.isActive():
            self.timer.stop()
            self.timer.start(1000 // self.frame_rate)

    def apply_bw_filter(self):
        if self.mode == "bw":
            self.mode = "normal"
            self.bw_button.setText("Black & White")
        else:
            self.mode = "bw"
            self.bw_button.setText("Normal")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
