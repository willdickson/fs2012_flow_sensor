from __future__ import print_function
import os
import sys
from PyQt5 import QtCore
from PyQt5 import QtGui 
from PyQt5 import QtWidgets
from mainwindow_ui import Ui_MainWindow

from data_reader import DataReader

class FlowSensorApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(FlowSensorApp,self).__init__(parent)
        self.timer_period = 20
        self.data_filename = 'flow_data.txt'
        self.data_pathname = os.path.join(os.path.abspath(os.curdir),'flow_data.txt')
        self.outfile = None

        self.setupUi(self)
        self.reader = DataReader('/dev/ttyUSB0')
        self.reader.start()
        self.lcd_number_list = [self.lcdNumber1, self.lcdNumber2]
        self.initialize_ui()

    def __del__(self):
        self.reader.stop()

    def initialize_ui(self):
        self.set_lcd_colors()
        self.timer = QtCore.QTimer()
        self.timer.start(self.timer_period)
        self.connect_ui_actions()

    def connect_ui_actions(self):
        self.timer.timeout.connect(self.on_timer)
        self.recordCheckBox.stateChanged.connect(self.on_record_changed)

    def on_record_changed(self,value):
        if value == QtCore.Qt.Checked:
            self.outfile = open(self.data_pathname,'w')
        else:
            self.outfile.close()
            self.outfile = None

    def on_timer(self):
        data = self.reader.get_data()
        if not data:
            return
        for lcd_number, flow in zip(self.lcd_number_list,data['flow']):
            flow_str = '{:0.2f}'.format(abs(flow))
            lcd_number.display(flow_str)
        if self.outfile is not None:
            self.outfile.write('{:0.4} '.format(data['t']))
            for flow in data['flow']:
                self.outfile.write('{:0.4} '.format(flow))
            self.outfile.write('\n')

    def set_lcd_colors(self):
        for lcd_number in self.lcd_number_list:
            palette = lcd_number.palette()
            palette.setColor(palette.WindowText, QtGui.QColor(0, 255, 100))
            palette.setColor(palette.Light, QtGui.QColor(0, 0, 0))
            palette.setColor(palette.Dark, QtGui.QColor(0, 0, 0))
            palette.setColor(palette.Background, QtGui.QColor(0, 0, 0))
            lcd_number.setPalette(palette)

def app_main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = FlowSensorApp()
    mainWindow.show()
    app.exec_()


# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    app_main()


