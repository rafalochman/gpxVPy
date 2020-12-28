import io
import os
import sys
import folium
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QApplication, QWidget, QVBoxLayout, QFileDialog, QLabel, \
    QSizePolicy
from PyQt5 import QtWebEngineWidgets, QtGui
import gpxpy
import mpu
import datetime
from datetime import datetime
import plotly.express as px
import pandas as pd
import logging

m = folium.Map()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.plot_widget = QtWebEngineWidgets.QWebEngineView()
        self.map_widget = QtWebEngineWidgets.QWebEngineView()
        self.elevation_label = QLabel()
        self.time_label = QLabel()
        self.distance_label = QLabel()
        self.route_name_label = QLabel()
        self.file_name_label = QLabel()
        self.save_label = QLabel()
        self.upload_gpx_button = QPushButton("upload gpx file")
        self.save_map_button = QPushButton("save map")
        self.sub_layout_right = QVBoxLayout()
        self.sub_layout_left = QVBoxLayout()
        self.layout = QHBoxLayout()
        self.init_window()
        self.logger = logging.getLogger("gpxViewer")
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler('logs.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.setStyleSheet(open('style.css').read())

    def init_window(self):
        self.setWindowTitle("GPX Viewer")
        self.resize(1300, 800)
        self.setWindowIcon(QtGui.QIcon('map_icon.png'))
        self.init_layout()

    def init_layout(self):
        self.sub_layout_left.setSpacing(10)
        self.sub_layout_left.setContentsMargins(20, 0, 0, 0)
        self.sub_layout_left.addStretch()
        self.layout.addLayout(self.sub_layout_left)
        self.layout.addLayout(self.sub_layout_right)
        self.upload_gpx_button.setFixedSize(120, 45)
        self.save_map_button.setObjectName("save_map_button")
        self.save_map_button.setFixedWidth(85)
        self.save_map_button.setContentsMargins(50, 50, 50, 50)
        self.save_map_button.setVisible(False)

        self.upload_gpx_button.clicked.connect(self.upload_gpx_button_handler)
        self.save_map_button.clicked.connect(self.save_map_handler)

        self.route_name_label.setMinimumWidth(160)
        self.file_name_label.setContentsMargins(0, 20, 0, 0)

        self.sub_layout_left.addWidget(self.upload_gpx_button)
        self.sub_layout_left.addWidget(self.file_name_label)
        self.sub_layout_left.addWidget(self.route_name_label)
        self.sub_layout_left.addWidget(self.distance_label)
        self.sub_layout_left.addWidget(self.time_label)
        self.sub_layout_left.addWidget(self.elevation_label)
        self.sub_layout_left.addStretch()
        self.sub_layout_left.addWidget(self.save_label)
        self.sub_layout_left.addWidget(self.save_map_button)

        self.map_widget.setMinimumSize(400, 400)
        self.map_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.map_widget.setContentsMargins(30, 30, 30, 30)
        global m
        m = folium.Map(
            location=[51.919438, 19.145136], zoom_start=5
        )
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.map_widget.setHtml(data.getvalue().decode())
        self.sub_layout_right.addWidget(self.map_widget)

        self.plot_widget.setMinimumHeight(80)
        self.plot_widget.setContentsMargins(30, 0, 30, 30)
        self.sub_layout_right.addWidget(self.plot_widget)

        self.setLayout(self.layout)

    def upload_gpx_button_handler(self):
        self.save_label.setText("")
        path = QFileDialog.getOpenFileName(None, "Select GPX file", "", "GPX files (*.gpx)")
        path = path[0]
        file_name = os.path.basename(path)
        self.file_name_label.setText("Selected file: " + file_name)
        self.file_name_label.setStyleSheet("color: black;")
        self.display_gpx(path)

    def save_map_handler(self):
        global m
        try:
            file_name = self.route_name_label.text().split()[-1] + ".html"
            m.save(file_name)
            self.save_label.setStyleSheet("color: black;")
            self.save_label.setText("File saved")
        except Exception as e:
            self.save_label.setStyleSheet("color: red;")
            self.save_label.setText("File not saved")
            self.logger.error(e)

    def on_time(self):
        self.save_label.setText("")

    def display_gpx(self, path):
        points = []
        points_time_ele = []
        tracks_name = []
        elevations_list = []
        try:
            gpx_file = open(path, 'r', encoding='utf8')
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                tracks_name.append(track.name)
                for segment in track.segments:
                    for point in segment.points:
                        points.append([point.latitude, point.longitude])
                        points_time_ele.append([point.time, point.elevation])
                        elevations_list.append(point.elevation)
        except Exception as e:
            self.file_name_label.setText("Selected wrong file")
            self.file_name_label.setStyleSheet("color: red;")
            self.logger.error(e)
            return

        center_lat = sum(p[0] for p in points) / len(points)
        center_lon = sum(p[1] for p in points) / len(points)

        global m
        m = folium.Map(
            location=[center_lat, center_lon]
        )
        folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)
        m.fit_bounds(points)
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.map_widget.setHtml(data.getvalue().decode())
        self.map_widget.update()
        self.route_name_label.setText("Route name: " + "     ".join(map(str, tracks_name)))

        distances_list = []
        distance = 0
        i = 0
        while i < len(points) - 1:
            distances_list.append(distance)
            distance = distance + mpu.haversine_distance((points[i][0], points[i][1]),
                                                         (points[i + 1][0], points[i + 1][1]))
            distance = round(distance, 2)
            i = i + 1
        self.distance_label.setText("Distance: " + str(distance) + " km")

        datetime_format = "%Y-%m-%d %H:%M:%S"
        start_time = points_time_ele[0][0].strftime(datetime_format)
        end_time = points_time_ele[len(points_time_ele) - 1][0].strftime(datetime_format)
        route_time = datetime.strptime(end_time, datetime_format) - datetime.strptime(start_time, datetime_format)
        self.time_label.setText("Time: " + str(route_time))

        elevation = 0
        i = 0
        while i < len(points_time_ele) - 1:
            if points_time_ele[i + 1][1] - points_time_ele[i][1] > 0.1:
                elevation = elevation + abs(points_time_ele[i + 1][1] - points_time_ele[i][1])
            i = i + 1

        self.elevation_label.setText("Elevation: " + str(round(elevation, 2)) + " m")

        df = pd.DataFrame(list(zip(elevations_list, distances_list)),
                          columns=['elevation', 'distance'])
        plot = px.line(df, x="distance", y="elevation")
        plot.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            margin=dict(t=0, l=0, b=0, r=0),
            font_size=9,
        )
        plot.update_xaxes(visible=False, fixedrange=True)
        plot.update_traces()
        self.plot_widget.setHtml(plot.to_html(include_plotlyjs='cdn', config=dict(displayModeBar=False)))
        self.save_map_button.setVisible(True)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
