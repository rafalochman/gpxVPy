import io
import os
import sys
import folium
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QApplication, QWidget, QVBoxLayout, QFileDialog, QLabel, \
    QSizePolicy
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
        self.layout = QHBoxLayout()
        self.sub_layout = QVBoxLayout()
        self.sub_layout.setSpacing(10)
        self.sub_layout.addStretch()
        self.layout.addLayout(self.sub_layout)

        self.upload_gpx_button = QPushButton("upload gpx file")
        self.upload_gpx_button.setFixedSize(100, 40)
        self.upload_gpx_button.clicked.connect(self.upload_gpx_button_handler)

        self.file_name_label = QLabel()

        self.route_name_label = QLabel("Nazwa trasy:")
        self.route_name_label.setMinimumWidth(200)

        self.distance_label = QLabel("Dystans:")

        self.time_label = QLabel("Czas:")
        self.elevation_label = QLabel("Przewyższenia:")

        self.sub_layout.addWidget(self.upload_gpx_button)
        self.sub_layout.addWidget(self.file_name_label)
        self.sub_layout.addWidget(self.route_name_label)
        self.sub_layout.addWidget(self.distance_label)
        self.sub_layout.addWidget(self.time_label)
        self.sub_layout.addWidget(self.elevation_label)

        self.sub_layout.addStretch()

        self.map_widget = QtWebEngineWidgets.QWebEngineView()
        self.map_widget.setMinimumSize(400, 400)
        self.map_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.map_widget.setContentsMargins(30, 30, 30, 30)
        m = folium.Map(
            location=[51.919438, 19.145136], zoom_start=5
        )
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.map_widget.setHtml(data.getvalue().decode())

        self.layout.addWidget(self.map_widget)

        self.setLayout(self.layout)

    def upload_gpx_button_handler(self):
        path = QFileDialog.getOpenFileName(None, "Select GPX file", "", "GPX files (*.gpx)")
        path = path[0]
        file_name = os.path.basename(path)
        self.file_name_label.setText("Wybrany plik: " + file_name)
        self.display_gpx_route(path)

    def display_gpx_route(self, path):
        gpx_file = open(path, 'r', encoding='utf8')
        gpx = gpxpy.parse(gpx_file)
        points = []
        tracks_name = []
        for track in gpx.tracks:
            tracks_name.append(track.name)
            for segment in track.segments:
                for point in segment.points:
                    points.append(tuple([point.latitude, point.longitude]))

        center_lat = sum(p[0] for p in points) / len(points)
        center_lon = sum(p[1] for p in points) / len(points)

        m = folium.Map(
            location=[center_lat, center_lon]
        )
        folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)
        m.fit_bounds(points)

        data = io.BytesIO()
        m.save(data, close_file=False)
        self.map_widget.setHtml(data.getvalue().decode())
        self.map_widget.update()
        self.route_name_label.setText("Nazwa trasy: " + "     ".join(map(str, tracks_name)))


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
