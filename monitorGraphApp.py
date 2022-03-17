from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys 
from random import randint
import _thread
import socket
import json

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        styles = {'color':'r', 'font-size':'20px'}
        self.graphWidget.setLabel('left', 'Force', **styles)
        self.graphWidget.setLabel('bottom', 'Sample', **styles)

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0), width=10)
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen, symbol='+', symbolSize=30, symbolBrush=('b'))

def receiveSampleAndUpdateDisplay( threadName, s, main):
    while True:
        s.listen(1)
        conn, addr = s.accept()
        while True:
            try:
                
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
                print()
                data = json.loads(data.decode())
                scaleValueRaw = int(data.get("scaleValueRaw"))

                main.x = main.x[1:]  # Remove the first y element.
                main.x.append(main.x[-1] + 1)  # Add a new value 1 higher than the last.

                main.y = main.y[1:]  # Remove the first
                main.y.append( scaleValueRaw)  # Add a new random value.

                main.data_line.setData(main.x, main.y)  # Update the data.

                print(scaleValueRaw)
            except:
                break
        conn.close()    
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 50000))
        _thread.start_new_thread(receiveSampleAndUpdateDisplay, ("Thread-1", s, main) )
    except:
        print("Error: unable to start thread")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# ADD CSV LOGGING