import time
from fs2012_flow_sensor import DataReader

port = '/dev/ttyACM0'
reader = DataReader(port)
reader.start()
for i in range(10):
    print(reader.get_data())
    time.sleep(0.1)
reader.stop()
