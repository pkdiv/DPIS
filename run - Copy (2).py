import sys
import time
from PyQt5 import uic
from PyQt5 import QtWidgets
from functools import partial
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFileDialog, QMessageBox

# Global Variables
name = "xcvxcv"
date = ""
gender = ""
fingerPrintFiles = []


class insertWindow(QDialog):
    def __init__(self):
        super(insertWindow, self).__init__()
        uic.loadUi("UI/mainWindow.ui", self)
        self.fingerObjLst = [self.lSmallButton, self.lRingButton, self.lMiddleButton, self.lIndexButton,
                             self.lThumbButton, self.rSmallButton, self.rRingButton, self.rMiddleButton,
                             self.rIndexButton, self.rThumbButton]
        self.fingerPrintFiles = [None for _ in range(10)]
        self.setup()

    def setup(self):
        self.genderInput.addItems(["Male", "Female", "Others"])

        for obj in self.fingerObjLst:
            obj.clicked.connect(partial(self.getFile, self.fingerObjLst.index(obj)))

        self.nextButton.clicked.connect(self.runFunction)

    def runFunction(self):
        allValidFiles = True
        # for path in self.fingerPrintFiles:
        #     if path == None or path == "":
        #         allValidFiles = False
        #         break



        if allValidFiles:
            global name
            global date
            global gender
            global fingerPrintFiles
            name = self.nameInput.toPlainText()
            date = self.dateInput.text()
            gender = self.genderInput.currentText()
            fingerPrintFiles = self.fingerPrintFiles
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Missing Files")
            msg.setInformativeText('Upload all the required files')
            msg.setWindowTitle("Error")
            msg.setFixedWidth(400)
            msg.exec_()

    def getFile(self, index):
        self.fingerPrintFiles[index] = QFileDialog.getOpenFileName()[0]
        if self.fingerPrintFiles[index] != "":
            self.fingerObjLst[index].setStyleSheet("background-color:#6D9886")
            print(self.fingerPrintFiles[index])


class runWindow(QDialog):
    def __init__(self):
        super(runWindow, self).__init__()
        uic.loadUi("UI/run.ui", self)
        self.startButton.clicked.connect(self.start)
        # pixmap = QPixmap("Image/icon.png")
        # self.userImage.setPixmap(pixmap)
        # self.resize(pixmap.width(), pixmap.height())

    def start(self):
        img = "Image/icon.png"
        self.userImage.setStyleSheet(f"background-image:url({img});  background-repeat: no-repeat; background-position: center;")
        # self.movie = QMovie("Image/gifimg.gif")
        # self.gifImage.setMovie(self.movie)
        self.animation = runAnimation()
        self.animation.start()

        # for img in fingerPrintFiles:


class welcomeWindow(QDialog):
    def __init__(self):
        super(welcomeWindow, self).__init__()
        uic.loadUi("UI/welcome.ui", self)
        pixmap = QPixmap("Image/icon.png")
        self.insertButton.clicked.connect(self.changeToInsert)
        self.welcomeWindow.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

    def changeToInsert(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

class runAnimation(QThread):
    def run(self):
        count = 0
        imgList = ["gif/10.png", "gif/11.png"]
        while True:
            runWindow.gifImage.setStyleSheet(f"background-image:url({imgList[count]});  background-repeat: no-repeat; background-position: center;")
            count += 1
            count %= 2
            time.sleep(0.1)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
welcomeWindow = welcomeWindow()
insertWindow = insertWindow()
runWindow = runWindow()
widget.addWidget(welcomeWindow)
widget.addWidget(insertWindow)
widget.addWidget(runWindow)
widget.setFixedHeight(600)
widget.setFixedWidth(950)
widget.show()
sys.exit(app.exec())
