import _thread
from math import trunc
import time
import socket
import json
from random import randint

def sendSample( threadName):
    delay = 1000
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('192.168.1.59', 50000))
        except:
            pass
        while True:
            try:
                f = open("/sys/module/scaleKernelDriver/parameters/scale_value", "r")
                value = f.read()
                f.close()
                scaleValue = str(value)
                scaleValueDataInJSON = json.dumps({"scaleValueRaw": scaleValue})
                print(scaleValueDataInJSON.encode())
                s.send(scaleValueDataInJSON.encode())
                time.sleep(0.01)
            except:
                s.close()
                break


if __name__ == "__main__":
    try:
        _thread.start_new_thread(sendSample, ("Thread-1", ) )
    except Exception as e:
        print("Error: unable to start thread or connect" + e)

    while True:
        pass