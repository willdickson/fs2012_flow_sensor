from __future__ import print_function
import sys
import time
import serial
import matplotlib
import matplotlib.pyplot as plt
import signal


class LivePlot(serial.Serial):

    ResetSleepDt = 0.5
    Baudrate = 115200

    def __init__(self,port,timeout=10.0):
        param = {'baudrate': self.Baudrate, 'timeout': timeout}
        super(LivePlot,self).__init__(port,**param)
        time.sleep(self.ResetSleepDt)


        self.window_size = 10.0
        self.data_file = 'data.txt'

        self.t_init =  time.time()
        self.t_list = []
        self.line_list = []

        self.running = False
        signal.signal(signal.SIGINT, self.sigint_handler)

        plt.ion()
        self.fig = plt.figure(1)
        self.ax = plt.subplot(111) 
        self.line, = plt.plot([0,1], [0,1],'b')
        plt.grid('on')
        plt.xlabel('t (sec)')
        plt.ylabel('flow  (L/min)')
        self.ax.set_xlim(0,self.window_size)
        self.ax.set_ylim(-0.01,2.01)
        plt.title("FS2012 Flow Sensor")
        self.line.set_xdata([])
        self.line.set_ydata([])
        self.fig.canvas.flush_events()


    def sigint_handler(self,signum,frame):
        self.running = False


    def raw_to_liter_per_min(self,raw_val):
        volt = 5.0*float(raw_val)/float(1023)
        return 0.4*(volt  - 0.045)

    def run(self):

        self.write('b\n')
        self.running = True

        with open(self.data_file, 'w') as fid:
            while self.running:
                have_data = False
                while self.in_waiting > 0:
                    # Not the best - throwing points away. Maybe put points in list, process later. 
                    line = self.readline()
                    have_data = True
                if have_data:
                    line = line.strip()
                    data = line.split(' ')
                    try:
                        t = data[0]
                        raw_val = data[1]
                    except IndexError:
                        continue
                    except ValueError:
                        continue

                    print('{0}, {1}'.format(t,raw_val))

                    t_elapsed = time.time() - self.t_init
                    self.t_list.append(t_elapsed)

                    liter_per_min = self.raw_to_liter_per_min(raw_val)
                    self.line_list.append(liter_per_min)

                    while (self.t_list[-1] - self.t_list[0]) > self.window_size:
                        self.t_list.pop(0)
                        self.line_list.pop(0)

                    self.line.set_xdata(self.t_list)
                    self.line.set_ydata(self.line_list)

                    xmin = self.t_list[0]
                    xmax = max(self.window_size, self.t_list[-1])

                    self.ax.set_xlim(xmin,xmax)
                    self.fig.canvas.flush_events()
                    #plt.pause(0.0001)
                    fid.write('{0} {1}\n'.format(t_elapsed, liter_per_min))

        print('quiting')
        self.write('\n')



# ---------------------------------------------------------------------------------------
if __name__ == '__main__':

    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = '/dev/ttyUSB0'

    liveplot = LivePlot(port=port)
    liveplot.run()



