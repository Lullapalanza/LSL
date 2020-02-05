from PyQt5.QtWidgets import *
from mono_connection import *


def setup_connections(window):
    grp_box0 = QGroupBox("Connection and properties", window)
    grp_box0.setFixedSize(390, 290)

    # Connection to Mono
    window.conn_text = QLabel("Mono program: ---------", grp_box0)
    window.conn_text.move(10, 60)
    window.conn_button = QPushButton("Connect to mono", grp_box0)
    window.conn_button.resize(145, 27)
    window.conn_button.clicked.connect(window.connect_to_mono)
    window.conn_button.move(230, 55)

    # Connection to Sourcemeter
    window.source_text = QLabel("Sourcemeter: ---------", grp_box0)
    window.source_text.move(10, 110)
    window.source_button = QPushButton("Connect to SM", grp_box0)
    window.source_button.resize(145, 27)
    window.source_button.clicked.connect(window.connect_to_SM)
    window.source_button.move(230, 105)

    # Set WL
    window.wl_text = QLabel("Wavelength: 500 ", grp_box0)
    window.wl_text.move(10, 160)
    window.new_wl_text = QLineEdit(grp_box0)
    window.new_wl_text.resize(50, 25)
    window.new_wl_text.move(170, 155)
    window.wl_button = QPushButton("Set wl", grp_box0)
    window.wl_button.clicked.connect(window.change_wl)
    window.wl_button.move(230, 155)

    # Shutter
    window.shutter_text = QLabel("Shutter: CLOSED", grp_box0)
    window.shutter_text.move(10, 210)
    window.shutter_open_button = QPushButton("Open", grp_box0)
    window.shutter_open_button.clicked.connect(window.open_shutter)
    window.shutter_open_button.move(150, 205)
    window.shutter_closed_button = QPushButton("Closed", grp_box0)
    window.shutter_closed_button.clicked.connect(window.close_shutter)
    window.shutter_closed_button.move(230, 205)

    window.test_button = QPushButton("Test Keithley", grp_box0)
    window.test_button.move(10, 255)
    window.test_button.clicked.connect(window.test_SM)

    return grp_box0