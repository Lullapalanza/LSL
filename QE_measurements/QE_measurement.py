from instrument import Instrument
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from win32gui import FindWindow
from win32api import SendMessage
from time import sleep
import serial
import random

BAUD = 9600

WM_SET_WAVE = 0x0400 + 0x0004
WM_SET_SHUTTER = 0x0400 + 0x0005;


class Window(QMainWindow):

    def setup_connections(self):
        grp_box0 = QGroupBox("Connection and properties", self)
        grp_box0.setFixedSize(390, 290)

        # Connection to Mono
        conn_text = QLabel("Mono program: ---------", grp_box0)
        conn_text.move(10, 60)
        conn_button = QPushButton("Connect to mono", grp_box0)
        conn_button.resize(145, 27)
        conn_button.clicked.connect(self.connect_to_mono)
        conn_button.move(230, 55)

        # Connection to Sourcemeter
        source_text = QLabel("Sourcemeter: ---------", grp_box0)
        source_text.move(10, 110)
        source_button = QPushButton("Connect to SM", grp_box0)
        source_button.resize(145, 27)
        source_button.clicked.connect(self.connect_to_SM)
        source_button.move(230, 105)

        # Set WL
        wl_text = QLabel("Wavelength: 500 ", grp_box0)
        wl_text.move(10, 160)
        new_wl_text = QLineEdit(grp_box0)
        new_wl_text.resize(50, 25)
        new_wl_text.move(170, 155)
        wl_button = QPushButton("Set wl", grp_box0)
        wl_button.clicked.connect(self.change_wl)
        wl_button.move(230, 155)

        # Shutter
        shutter_text = QLabel("Shutter: CLOSED", grp_box0)
        shutter_text.move(10, 210)
        shutter_open_button = QPushButton("Open", grp_box0)
        shutter_open_button.clicked.connect(self.open_shutter)
        shutter_open_button.move(150, 205)
        shutter_closed_button = QPushButton("Closed", grp_box0)
        shutter_closed_button.clicked.connect(self.close_shutter)
        shutter_closed_button.move(230, 205)

        return grp_box0
    
    def setup_measurement(self):
        grp_box1 = QGroupBox("Measurement", self)
        grp_box1.setFixedSize(390, 290)

        # Start WL
        start_wl_Label = QLabel("Start wl: 500 ", grp_box1)
        start_wl_Label.move(10, 60)

        start_wl_LineEdit = QLineEdit(grp_box1)
        start_wl_LineEdit.resize(50, 25)
        start_wl_LineEdit.move(160, 55)

        start_wl_Button = QPushButton("Set start wl", grp_box1)
        start_wl_Button.resize(130, 27)
        start_wl_Button.clicked.connect(self.set_start_wl)
        start_wl_Button.move(220, 55)

        # End Wl
        end_wl_Label = QLabel("End wl: 1050", grp_box1)
        end_wl_Label.move(10, 110)

        end_wl_LineEdit = QLineEdit(grp_box1)
        end_wl_LineEdit.resize(50, 25)
        end_wl_LineEdit.move(160, 105)

        end_wl_Button = QPushButton("Set end wl", grp_box1)
        end_wl_Button.resize(130, 27)
        end_wl_Button.clicked.connect(self.set_end_wl)
        end_wl_Button.move(220, 105)

        # Step
        step_Label = QLabel("Step: 10 ", grp_box1)
        step_Label.move(10, 160)

        step_LineEdit = QLineEdit(grp_box1)
        step_LineEdit.resize(50, 25)
        step_LineEdit.move(160, 155)

        step_Button = QPushButton("Set step", grp_box1)
        step_Button.resize(130, 27)
        step_Button.clicked.connect(self.set_step)
        step_Button.move(220, 155)

        start_Button = QPushButton("Start", grp_box1)
        start_Button.clicked.connect(self.start_measurement)
        start_Button.resize(130, 27)
        start_Button.move(220, 210)
        
        return grp_box1

    def setup_graph(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.subplot = self.figure.add_subplot(111)
        self.canvas.draw()
        return self.canvas
    
    def setup_save(self):
        grp_box2 = QGroupBox("Save graph", self)
        grp_box2.setFixedSize(780, 120)
        save_Button = QPushButton("Save", grp_box2)
        save_Button.clicked.connect(self.save)
        save_Button.move(30, 60)
        return grp_box2
    
    def setup_main_frame(self):
        main_frame = QWidget()

        main_hbox = QHBoxLayout()
        main_vbox0 = QVBoxLayout()
        main_vbox1 = QVBoxLayout()

        conn_box = self.setup_connections()
        measurement_box = self.setup_measurement()
        canvas = self.setup_graph()
        save_box = self.setup_save()
               
        main_vbox0.addWidget(conn_box, 1)
        main_vbox0.addWidget(measurement_box, 1)
        main_vbox1.addWidget(canvas, 1)
        main_vbox1.addWidget(save_box, 1)

        main_hbox.addLayout(main_vbox0, 1)
        main_hbox.addLayout(main_vbox1, 1)

        main_frame.setLayout(main_hbox)
        self.setCentralWidget(main_frame)

    def initUI(self):
        self.setFixedSize(1200, 600)
        self.setWindowTitle("QE Measurement")
        self.setStyleSheet("font: 12pt Consolas;")

        self.setup_main_frame()

    #######
    def connect_to_mono(self):
        self.hwnd = FindWindow(None, 'Mono')
        if self.hwnd != 0:
            self.connected = True
            self.conn_text.setText("Mono program: connected")
            SendMessage(self.hwnd, self.WM_SET_WAVE, 500, 0)
            SendMessage(self.hwnd, self.WM_SET_SHUTTER, 0, 0)
        else:
            print("Didn't connect")

    def connect_to_SM(self):
        if self.connected:
            self.keithley = Instrument()
            self.source_text.setText("Sourcemeter: connected")

    def change_wl(self):
        if self.connected:
            try:
                self.new_wl = int(self.new_wl_text.text())
                if 100 < self.new_wl < 2000:
                    SendMessage(self.hwnd, self.WM_SET_WAVE, self.new_wl, 0)
                    self.wl_text.setText("Wavelength: " + str(self.new_wl))
            except ValueError:
                print("Please enter an int")

    def open_shutter(self):
        if self.connected:
            SendMessage(self.hwnd, self.WM_SET_SHUTTER, 1, 0)
            self.shutter_text.setText("Shutter:  OPEN ")

    def close_shutter(self):
        if self.connected:
            SendMessage(self.hwnd, self.WM_SET_SHUTTER, 0, 0)
            self.shutter_text.setText("Shutter: CLOSED")

    def reset(self):
        if self.connected:
            self.keithley.shutdown()

    def set_start_wl(self):
        self.start_wl = int(self.start_wl_LineEdit.text())
        if 100 < self.start_wl < 2500:
            self.start_wl_Label.setText("Start wl: " + str(self.start_wl))

    def set_end_wl(self):
        self.end_wl = int(self.end_wl_LineEdit.text())
        if self.start_wl < self.end_wl < 2500:
            self.end_wl_Label.setText("End wl: " + str(self.end_wl))

    def set_step(self):
        self.step = int(self.step_LineEdit.text())
        self.step_Label.setText("Step: " + str(self.step))

    def update(self):
        self.canvas.draw()
        print("Hello")

    def measure_VA(self, wl):
        ser = serial.Serial("COM7", BAUD, timeout=2)
        if ser.isOpen():
            ser.write("*TST?".encode("ascii"))
            out = ser.read()
            print(out)
            ser.close()
            # exit()
        # try:
        # self.keithley.apply_voltage()
        # sleep(0.5)
        # self.keithley.source_voltage_range = 1e-2
        # sleep(0.5)
        # self.keithley.compliance_current = 0.1
        # sleep(0.5)
        # self.keithley.source_voltage = 0
        # sleep(0.5)
        # self.keithley.enable_source()
        # print("1/2 of setup for VA")
        # sleep(1)

        # self.keithley.measure_current()
        # sleep(1)
        # self.keithley.sample_continuously()
        # sleep(1)
        # self.keithley.set_timed_arm(0.1)
        # print("VA setup done")
        # sleep(1)

        # self.keithley.ramp_to_voltage(0.01)
        # sleep(1)
        # print(self.keithley.current)
        # sleep(1)
        # self.keithley.ramp_to_voltage(0.02)
        # sleep(1)
        # print(self.keithley.current)
        # sleep(1)
        # self.keithley.ramp_to_voltage(0.03)
        # sleep(1)
        # print(self.keithley.current)
        # sleep(1)
        # print(self.keithley.error)
        # finally:
        # self.keithley.shutdown()

    def start_measurement(self):

        if self.test:
            self.data = []
            self.wls = []
            for i in range((self.end_wl - self.start_wl) // self.step + 1):
                self.wls.append(self.start_wl + self.step * i)
            for wl in self.wls:
                print(wl)

                sleep(0.1)
                if wl in self.VA_wls:
                    self.measure_VA(wl)
                    sleep(5)
                current = random.randint(0, 100) + wl
                self.data.append(current)
                self.subplot.clear()
                self.subplot.plot(self.wls[0:len(self.data)], self.data)
                self.canvas.draw()
                self.canvas.flush_events()

        elif self.connected:
            self.data = []
            self.wls = []
            for i in range((self.end_wl - self.start_wl) // self.step + 1):
                self.wls.append(self.start_wl + self.step * i)

            try:
                # self.keithley.apply_voltage()
                # self.keithley.source_voltage_range = 1e-3
                # self.keithley.compliance_voltage = 1
                self.keithley.setup()
                self.keithley.source_mode("V")
                self.keithley.source_value(0)
                self.keithley.source_enabled(True)

                # self.keithley.measure_current()
                # self.keithley.sample_continuously()
                # self.keithley.set_timed_arm(0.1)

                SendMessage(self.hwnd, self.WM_SET_SHUTTER, 1, 0)
                SendMessage(self.hwnd, self.WM_SET_WAVE, self.start_wl, 0)
                sleep(1)

                for wl in self.wls:
                    print(wl)
                    SendMessage(self.hwnd, self.WM_SET_WAVE, wl, 0)
                    sleep(0.1)
                    current = self.keithley.current
                    self.data.append(current)
                    self.subplot.clear()
                    self.subplot.plot(self.wls[0:len(self.data)], self.data)
                    self.canvas.draw()
                    self.canvas.flush_events()
            finally:
                SendMessage(self.hwnd, self.WM_SET_SHUTTER, 0, 0)
                self.keithley.shutdown()

    def save(self):
        self.file_name = QFileDialog.getSaveFileName(self, 'Save File')
        self.file = open(self.file_name[0], 'w')
        for i in range(len(self.wls)):
            self.file.write(str(self.wls[i]) + '\t' + str(self.data[i]) + '\n')
        self.file.close()
    #####

    def __init__(self, parent=None):
        self.VA_wls = [600, 1000]

        QWidget.__init__(self, parent=parent)
        self.initUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())