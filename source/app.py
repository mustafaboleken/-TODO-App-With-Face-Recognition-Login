import sys, os
import face_recognition
import numpy as np
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import uic

from ui_main_window2 import *

class Authentication(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.known_face_encodings = []
        self.known_face_names = []

        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.name = ""
        self.process_this_frame = True


        try:
            for file in os.listdir("../face-database"):
                if file.endswith(".jpg"):
                    self.known_face_names.append(file.strip(".jpg"))
                    temp = face_recognition.load_image_file("../face-database/"+file)
                    self.known_face_encodings.append( face_recognition.face_encodings(temp)[0] )
        except IndexError:
            print("Error: Known faces cannot be loaded!")
            quit()

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.cap = cv2.VideoCapture(0)
        self.timer.start(20)

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        frame = image
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            print(self.face_encodings)
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                self.name = "Unknown"

                # use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    self.name = self.known_face_names[best_match_index]
                    # face matched
                    print(self.name)
                    self.controlTimer()

                self.face_names.append(self.name)

        self.process_this_frame = not self.process_this_frame


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
        cv2.destroyAllWindows()
        self.cap.release()
        # update control_bt text
        self.switch_window.emit(self.name)


class Login(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()
    switch_window1 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('TODO App')
        self.resize(300, 400)

        layout = QtWidgets.QGridLayout()

        label = QLabel(self)
        pixmap = QPixmap('../others/icon.png')
        label.setPixmap(pixmap)

        self.loginButton = QtWidgets.QPushButton('Login')
        self.loginButton.clicked.connect(self.login)

        self.registerButton = QtWidgets.QPushButton('Register')
        self.registerButton.clicked.connect(self.register)

        layout.addWidget(label)
        layout.addWidget(self.loginButton)
        layout.addWidget(self.registerButton)

        self.setLayout(layout)

    def login(self):
        self.switch_window.emit()

    def register(self):
    	self.switch_window1.emit()

class Register(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Register')

        layout = QtWidgets.QGridLayout()

        self.loginButton = QtWidgets.QPushButton('Login')
        self.loginButton.clicked.connect(self.login)

        self.registerButton = QtWidgets.QPushButton('Register')
        self.registerButton.clicked.connect(self.login)

        layout.addWidget(self.loginButton)
        layout.addWidget(self.registerButton)

        self.setLayout(layout)

    def login(self):
        self.switch_window.emit()


class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = Login()
        self.login.switch_window.connect(self.show_main)
        self.login.switch_window1.connect(self.show_register)
        self.login.show()

    def show_register(self):
    	os.system('python register.py')

    def show_main(self):
        self.window = Authentication()
        self.window.switch_window.connect(self.show_window_two)
        self.login.close()
        self.window.show()

    def show_window_two(self, text):
        self.window.close()
        os.system('python todo.py ' + text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
