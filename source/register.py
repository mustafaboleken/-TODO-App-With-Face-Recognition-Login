# import system module
import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

# import Opencv module
import cv2

from ui_main_window import *

class RegisterWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)
        self.cap = cv2.VideoCapture(0)
        self.timer.start(20)
        self.ui.control_bt.setText("Register")


    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        self.frame = image
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        self.timer.stop()
        # release video capture
        username = self.ui.input.text()
        if(username == ""):
            username = "anonymous"
        cv2.imwrite('../face-database/'+ username +'.jpg',self.frame)
        cv2.destroyAllWindows()
        self.cap.release()
        # update control_bt text
        quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = RegisterWindow()
    mainWindow.show()

    sys.exit(app.exec_())
