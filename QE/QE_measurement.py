from instrument import Instrument
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import json

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
        self.conn_text = QLabel("Mono program: ---------", grp_box0)
        self.conn_text.move(10, 60)
        self.conn_button = QPushButton("Connect to mono", grp_box0)
        self.conn_button.resize(145, 27)
        self.conn_button.clicked.connect(self.connect_to_mono)
        self.conn_button.move(230, 55)

        # Connection to Sourcemeter
        self.source_text = QLabel("Sourcemeter: ---------", grp_box0)
        self.source_text.move(10, 110)
        self.source_button = QPushButton("Connect to SM", grp_box0)
        self.source_button.resize(145, 27)
        self.source_button.clicked.connect(self.connect_to_SM)
        self.source_button.move(230, 105)

        # Set WL
        self.wl_text = QLabel("Wavelength: 500 ", grp_box0)
        self.wl_text.move(10, 160)
        self.new_wl_text = QLineEdit(grp_box0)
        self.new_wl_text.resize(50, 25)
        self.new_wl_text.move(170, 155)
        self.wl_button = QPushButton("Set wl", grp_box0)
        self.wl_button.clicked.connect(self.change_wl)
        self.wl_button.move(230, 155)

        # Shutter
        self.shutter_text = QLabel("Shutter: CLOSED", grp_box0)
        self.shutter_text.move(10, 210)
        self.shutter_open_button = QPushButton("Open", grp_box0)
        self.shutter_open_button.clicked.connect(self.open_shutter)
        self.shutter_open_button.move(150, 205)
        self.shutter_closed_button = QPushButton("Closed", grp_box0)
        self.shutter_closed_button.clicked.connect(self.close_shutter)
        self.shutter_closed_button.move(230, 205)
        
        self.test_button = QPushButton("Test Keithley", grp_box0)
        self.test_button.move(10, 255)
        self.test_button.clicked.connect(self.test_SM)

        return grp_box0
    
    def setup_measurement(self):
        grp_box1 = QGroupBox("Measurement", self)
        grp_box1.setFixedSize(390, 290)

        # Start WL
        self.start_wl_Label = QLabel("Start wl: 500 ", grp_box1)
        self.start_wl_Label.move(10, 60)

        self.start_wl_LineEdit = QLineEdit(grp_box1)
        self.start_wl_LineEdit.resize(50, 25)
        self.start_wl_LineEdit.move(160, 55)

        self.start_wl_Button = QPushButton("Set start wl", grp_box1)
        self.start_wl_Button.resize(130, 27)
        self.start_wl_Button.clicked.connect(self.set_start_wl)
        self.start_wl_Button.move(220, 55)

        # End Wl
        self.end_wl_Label = QLabel("End wl: 1050", grp_box1)
        self.end_wl_Label.move(10, 110)

        self.end_wl_LineEdit = QLineEdit(grp_box1)
        self.end_wl_LineEdit.resize(50, 25)
        self.end_wl_LineEdit.move(160, 105)

        self.end_wl_Button = QPushButton("Set end wl", grp_box1)
        self.end_wl_Button.resize(130, 27)
        self.end_wl_Button.clicked.connect(self.set_end_wl)
        self.end_wl_Button.move(220, 105)

        # Step
        self.step_Label = QLabel("Step: 10 ", grp_box1)
        self.step_Label.move(10, 160)

        self.step_LineEdit = QLineEdit(grp_box1)
        self.step_LineEdit.resize(50, 25)
        self.step_LineEdit.move(160, 155)

        self.step_Button = QPushButton("Set step", grp_box1)
        self.step_Button.resize(130, 27)
        self.step_Button.clicked.connect(self.set_step)
        self.step_Button.move(220, 155)

        self.start_Button = QPushButton("Start", grp_box1)
        self.start_Button.clicked.connect(self.start_measurement)
        self.start_Button.resize(130, 27)
        self.start_Button.move(220, 245)

        self.set_Uedit = QLineEdit(grp_box1)
        self.set_Uedit.resize(50, 25)
        self.set_Uedit.move(160, 210)

        self.Uedit_button = QPushButton("Set voltage", grp_box1)
        self.Uedit_button.resize(130, 27)
        self.Uedit_button.clicked.connect(self.set_voltage)
        self.Uedit_button.move(220, 210)
        
        return grp_box1
        
    def test_SM(self):
        self.VA_wls = [400, 500, 600, 700, 800, 900, 1000]
        if self.keithley:
            self.keithley.write("*TST?")
            print(self.keithley.read())

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
            SendMessage(self.hwnd, WM_SET_WAVE, 500, 0)
            SendMessage(self.hwnd, WM_SET_SHUTTER, 0, 0)
        else:
            print("Didn't connect")

    def connect_to_SM(self):
        # if self.connected:
        self.keithley = Instrument.Instrument()
        print("setting up")
        self.keithley.setup(arm=0.1, arm_counts=1, trig_counts=1)
        print("source mode change")
        self.keithley.source_mode("V")
        print("measure current")
        self.keithley.measure_current()
        print("comp current")
        self.keithley.set_compliance_current(current=0.003)
        print("source val")
        self.source_text.setText("Sourcemeter: connected")

    def change_wl(self):
        if self.connected:
            try:
                self.new_wl = int(self.new_wl_text.text())
                if 100 < self.new_wl < 2000:
                    SendMessage(self.hwnd, WM_SET_WAVE, self.new_wl, 0)
                    self.wl_text.setText("Wavelength: " + str(self.new_wl))
            except ValueError:
                print("Please enter an int")

    def open_shutter(self):
        if self.connected:
            SendMessage(self.hwnd, WM_SET_SHUTTER, 1, 0)
            self.shutter_text.setText("Shutter:  OPEN ")

    def close_shutter(self):
        if self.connected:
            SendMessage(self.hwnd, WM_SET_SHUTTER, 0, 0)
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

    def set_voltage(self):
        self.voltage = float(self.set_Uedit.text())

    def update(self):
        self.canvas.draw()
        print("Hello")

    def measure_VA(self, wl):
        self.VA_wls.remove(wl)
        volt_data = []
        curr_data = []
        self.keithley.source_value(0)
        sleep(5)
        temp_val = self.keithley.get_measurement()
        V = 0
        while temp_val < 0.003 and V <= 1.5:
            self.keithley.source_value(V)
            sleep(1)
            temp_val = self.keithley.get_measurement()
            sleep(1)
            print(f"Measuring VA {temp_val}")
            volt_data.append(V)
            curr_data.append(temp_val)
            V += 0.1
            
        self.keithley.source_value(0)
        sleep(5)
        temp_val = self.keithley.get_measurement()
        V = 0
        while temp_val > -10**(-5) and V >= -2:
            self.keithley.source_value(V)
            sleep(1)
            temp_val = self.keithley.get_measurement()
            sleep(1)
            print(f"Measuring VA {temp_val}")
            volt_data.append(V)
            curr_data.append(temp_val)
            V -= 0.1
            
        self.keithley.source_value(0)
        sleep(5)
        self.content.update({wl: [volt_data, curr_data]})

    def start_measurement(self):
        if self.test:
            self.data = []
            self.wls = []
            for i in range((self.end_wl - self.start_wl) // self.step + 1):
                self.wls.append(self.start_wl + self.step * i)
             
             
            print("setting up")
            self.keithley.setup()
            print("source mode change")
            self.keithley.source_mode("V")
            print("measure current")
            self.keithley.measure_current()
            print("comp current")
            self.keithley.set_compliance_current()
            print("source val")
            self.keithley.source_value(0)
            self.keithley.source_enabled(True)
            sleep(5)
            
            for wl in self.wls:
                print(wl)
                sleep(0.1)
                if wl in self.VA_wls:
                    self.measure_VA(wl)
                current = random.randint(0, 100) + wl
                self.data.append(current)
                self.subplot.clear()
                self.subplot.plot(self.wls[0:len(self.data)], self.data)
                self.canvas.draw()
                self.canvas.flush_events()
            
            print(self.keithley.source_enabled(False))
            self.content.update({f"spectrum_{self.voltage}": [self.wls, self.data]})
            
        elif self.connected:
            self.data = []
            self.wls = []
            for i in range((self.end_wl - self.start_wl) // self.step + 1):
                self.wls.append(self.start_wl + self.step * i)

            try:
                self.keithley.source_value(self.voltage)
                self.keithley.source_enabled(True)

                SendMessage(self.hwnd, WM_SET_SHUTTER, 1, 0)
                SendMessage(self.hwnd, WM_SET_WAVE, self.start_wl, 0)
                sleep(1)

                for wl in self.wls:
                    print(wl)
                    SendMessage(self.hwnd, WM_SET_WAVE, wl, 0)
                    sleep(0.1)
                    current = self.keithley.get_measurement()
                    self.data.append(current)
                    self.subplot.clear()
                    self.subplot.plot(self.wls[0:len(self.data)], self.data)
                    self.canvas.draw()
                    self.canvas.flush_events()
                    
                    #if wl in self.VA_wls:
                    #    self.measure_VA(wl)
            finally:
                SendMessage(self.hwnd, WM_SET_SHUTTER, 0, 0)
                self.keithley.source_value(0)
                self.keithley.source_enabled(False)
                self.content.update({"Spectrum": [self.wls, self.data]})

    def save(self):
        print(self.content)
        file_name = QFileDialog.getSaveFileName(self, 'Save File')
        if file_name != ('', ''):
            file = open(f"{file_name[0]}.json", 'w')
            json.dump(self.content, file)
            file.close()
        self.content = {}
            
    def closeEvent(self, event):
        if self.keithley:
            self.keithley.close()
        print("Closing app")

    def __init__(self, parent=None):
        self.VA_wls = []
        self.connected = False
        self.test = False
        self.start_wl = 500
        self.end_wl = 1050
        self.step = 10
        self.keithley = None
        self.content = {}

        QWidget.__init__(self, parent=parent)
        self.initUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())