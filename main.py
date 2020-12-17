import io
import sys
import folium
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QApplication, QWidget, QVBoxLayout
from PyQt5 import QtWebEngineWidgets


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

        sub_layout.addWidget(upload_gpx_button)
        sub_layout.addWidget(show_route_button)
        sub_layout.addStretch()

        map_widget = QtWebEngineWidgets.QWebEngineView()
        map_widget.setContentsMargins(30, 30, 30, 30)
        m = folium.Map(
            location=[51.919438, 19.145136], zoom_start=5
        )
        data = io.BytesIO()
        m.save(data, close_file=False)
        map_widget.setHtml(data.getvalue().decode())

        layout.addWidget(map_widget)

        self.setLayout(layout)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
