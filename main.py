import io
import os
import sys
import folium
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QApplication, QWidget, QVBoxLayout, QFileDialog, QLabel
from PyQt5 import QtWebEngineWidgets
import gpxpy


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

        self.upload_gpx_button = QPushButton("upload gpx file")
        self.upload_gpx_button.setFixedSize(100, 40)
        self.upload_gpx_button.clicked.connect(self.upload_gpx_button_handler)

        self.show_route_button = QPushButton("show route")
        self.show_route_button.setFixedSize(100, 40)

        self.file_name_label = QLabel()

        sub_layout.addWidget(self.upload_gpx_button)
        sub_layout.addWidget(self.file_name_label)
        sub_layout.addWidget(self.show_route_button)
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

    def upload_gpx_button_handler(self):
        path = QFileDialog.getOpenFileName(None, "Select GPX file", "", "GPX files (*.gpx)")
        path = path[0]
        file_name = os.path.basename(path)
        self.file_name_label.setText(file_name)

        gpx_file = open(path, 'r')
        gpx = gpxpy.parse(gpx_file)
        points_lat_lng = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points_lat_lng.append(tuple([point.latitude, point.longitude]))


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
