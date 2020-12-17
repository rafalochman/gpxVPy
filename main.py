import sys
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QApplication, QWidget, QVBoxLayout


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.init_window()

    def init_window(self):
        self.setWindowTitle("GPX Viewer")
        self.resize(1300, 700)
        self.init_layout()

    def init_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(50)
        sub_layout = QVBoxLayout()
        sub_layout.addStretch()
        layout.addLayout(sub_layout)

        upload_gpx_button = QPushButton("upload gpx file")
        show_route_button = QPushButton("show route")
        upload_gpx_button.setFixedSize(100, 40)
        show_route_button.setFixedSize(100, 40)

        map_widget = QPushButton()
        map_widget.setFixedSize(700, 500)

        sub_layout.addWidget(upload_gpx_button)
        sub_layout.addWidget(show_route_button)
        sub_layout.addStretch()
        layout.addWidget(map_widget)

        self.setLayout(layout)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
