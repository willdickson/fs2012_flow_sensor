from __future__ import print_function
import sys
import time
import serial
import threading
import signal

class DataReader(serial.Serial):

    ResetSleepDt = 0.5
    Baudrate = 115200

    def __init__(self,port,timeout=10.0):
        param = {'baudrate': self.Baudrate, 'timeout': timeout}
        super(DataReader,self).__init__(port,**param)
        time.sleep(self.ResetSleepDt)
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.receiver)
        self.thread.daemon = True
        self.running = False
        self.data = {}

    def receiver(self):
        done = False
        while not done:
            line = []
            with self.lock:
                done = not self.running
            while self.in_waiting > 0:
                line = self.readline()
            if line:
                line = line.strip()
                data = line.split(' ')
                try:
                    t = 1.0e-3*int(data[0])
                    raw_list = [float(x) for x in data[1:]]
                except IndexError:
                    continue
                except ValueError:
                    continue
                flow_list = [self.raw_to_liter_per_min(x) for x in raw_list]
                with self.lock:
                    self.data = {'t':t, 'flow': flow_list}

    def stop(self):
        with self.lock:
            self.running = False 
        self.thread.join()

    def start(self):
        if not self.running:
            self.running = True
            self.thread.start()

    def raw_to_liter_per_min(self,raw_val):
        volt = 5.0*float(raw_val)/float(1023)
        return 0.4*(volt  - 0.045)

    def get_data(self):
        with self.lock:
            data = dict(self.data)
        return data

# ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = '/dev/ttyUSB0'
    reader = DataReader(port)
    reader.start()
    for i in range(10):
        print(reader.get_data())
        time.sleep(1.0)
    reader.stop()








