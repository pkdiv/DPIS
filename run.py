import os
import sys
import time
from api import Api
from PyQt5 import uic
from PyQt5 import QtWidgets
from ridge_count import test
from functools import partial
from DB.DBapi import DBConnect
from match.match import FingerprintMatch
from PyQt5.QtGui import QPixmap, QMovie, QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFileDialog, QMessageBox



# Global Variables
name = ""
date = ""
gender = ""
fingerPrintFiles = [None for _ in range(10)]
ridgeCount = []
type = ['A', 'L', 'R', 'T', 'W']
fingerPrintType = []
imgpath = ""
row=""


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
        detailsPresent = True
        for path in self.fingerPrintFiles:
            if path == None or path == "":
                detailsPresent = False
                break

        self.name = self.nameInput.toPlainText()
        self.date = self.dateInput.text()
        self.gender = self.genderInput.currentText()

        if self.name in [None, ""] or self.date in [None, ""] or self.gender in [None, ""]:
            detailsPresent = False


        if detailsPresent:
            global name
            global date
            global gender
            global fingerPrintFiles
            name  = self.name
            date = self.date
            gender = self.gender
            fingerPrintFiles = self.fingerPrintFiles
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Missing Details")
            msg.setInformativeText('Enter the required details and upload files')
            msg.setWindowTitle("Error")
            msg.setFixedWidth(400)
            msg.exec_()

    def getFile(self, index):
        self.fingerPrintFiles[index] = QFileDialog.getOpenFileName()[0]
        if self.fingerPrintFiles[index] != "":
            self.fingerObjLst[index].setStyleSheet("background-color:#6D9886")


class runWindow(QDialog):
    def __init__(self):
        super(runWindow, self).__init__()
        uic.loadUi("UI/run.ui", self)
        img = "Image/icon.png"
        self.startButton.clicked.connect(self.start)
        self.storeButton.clicked.connect(self.storeData)
        self.doneButton.clicked.connect(self.restoreToScreen)
        self.gifImage.setStyleSheet(f"background-image:url({img});  background-repeat: no-repeat; background-position: center;")
        self.userImage.setStyleSheet(f"background-image:url({img});  background-repeat: no-repeat; background-position: center;")
        self.resultLabel = [self.lSmallResult, self.lRingResult, self.lMiddleResult, self.lIndexResult, self.lThumbResult, self.rSmallResult, self.rRingResult, self.rMiddleResult, self.rIndexResult, self.rThumbResult]
        self.storeButton.setEnabled(False)
        self.doneButton.setEnabled(False)

    def start(self):
        img = "Image/icon.png"
        self.userImage.setStyleSheet(f"background-image:url({img});  background-repeat: no-repeat; background-position: center;")
        self.startButton.setEnabled(False)
        self.animation = runAnimation()
        self.animation.start()
        self.classify = classify()
        self.classify.start()
        self.classify.finished.connect(self.finishClassify)

    def finishClassify(self):
        self.animation.terminate()
        self.storeButton.setEnabled(True)

    def storeData(self):
        global name
        global date
        global gender
        global ridgeCount
        global fingerPrintFiles
        global fingerPrintType

        if gender == "Male":
            gender = 'M'
        elif gender == "Female":
            gender = 'F'
        else:
            gender = 'O'

        formatDate = date.split("/")[::-1]
        newDate = "-".join(formatDate)

        details = {
            'name' : name,
            'dob' : newDate,
            'gender' : 'M',
            'images' : fingerPrintFiles,
            'ridgecounts': ridgeCount,
            'types': fingerPrintType
        }

        dbObject = DBConnect()
        result = dbObject.insertData(details)
        self.doneButton.setEnabled(True)

    def restoreToScreen(self):
        widget.setCurrentIndex(widget.currentIndex()-2)


class welcomeWindow(QDialog):
    def __init__(self):
        super(welcomeWindow, self).__init__()
        uic.loadUi("UI/welcome.ui", self)
        pixmap = QPixmap("Image/icon.png")
        self.insertButton.clicked.connect(self.changeToInsert)
        self.welcomeWindow.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.searchButton.clicked.connect(self.changeToSearch)

    def changeToInsert(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def changeToSearch(self):
        widget.setCurrentIndex(widget.currentIndex()+3)


class runAnimation(QThread):
    def run(self):
        count = 0
        imgList = ["gif/" + x for x in os.listdir("./gif")]
        while True:
            runWindow.gifImage.setStyleSheet(f"background-image:url({imgList[count]});  background-repeat: no-repeat; background-position: center;")
            count += 1
            count %= len(imgList)
            time.sleep(0.05)


class classify(QThread):
    # signal = pyqtSignal()
    def run(self):
        global fingerPrintType
        api = Api()
        index = 0
        for img in fingerPrintFiles:
            runWindow.userImage.setStyleSheet(f"background-image:url({img});  background-repeat: no-repeat; background-position: center;")
            fingerPrintType.append(api.call(img))
            ridgeCount.append(test.count_ridge(img))
            runWindow.resultLabel[index].setText(str(fingerPrintType[index]) + " " + str(ridgeCount[index]))
            index += 1


class searchWindow(QDialog):
    def __init__(self):
        img = "Image/icon.png"
        super(searchWindow, self).__init__()
        uic.loadUi("UI/search.ui", self)
        self.uploadButton.clicked.connect(self.fileUpload)
        self.searchButton.clicked.connect(self.search)
        self.searchButton.setEnabled(False)
        self.gifImage.setStyleSheet(f"background-image:url({img});  background-repeat: no-repeat; background-position: center;")
        self.userImage.setStyleSheet(f"background-image:url({img});  background-repeat: no-repeat; background-position: center;")

    def fileUpload(self):
        self.file =  QFileDialog.getOpenFileName()[0]
        if not (self.file == None or self.file == "") :
            self.uploadButton.setStyleSheet("background-color:#6D9886")
            self.searchButton.setEnabled(True)
            print

    def search(self):
        self.animation = runSearchAnimation()
        self.animation.start()
        self.userImage.setStyleSheet(f"background-image:url({self.file});  background-repeat: no-repeat; background-position: center;")
        if self.file == None or self.file == "":
            self.fileUploadError()
        else:
            self.searchFinger = searchFinger()
            self.searchFinger.start()
            self.searchFinger.finished.connect(self.finishSearch)

            db = DBConnect()
            result = db.getDetails(row)

    def finishSearch(self):
        global row
        db = DBConnect()
        result = db.getDetails(row)
        self.animation.terminate()
        self.nameBox.setText(result[1])
        self.dobBox.setText(str(result[2]))
        self.genderBox.setText(result[3])

    def fileUploadError(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Missing Files")
        msg.setInformativeText('Upload an image file to search')
        msg.setWindowTitle("Error")
        msg.setFixedWidth(400)
        msg.exec_()

class searchFinger(QThread):
    def run(self):
        global row
        self.match = FingerprintMatch('remotemysql.com','XMOhqXsSa4', 'XMOhqXsSa4','QbmL0ZttoO','E:/DPIS/finger.png')
        row = self.match.find_match()


class runSearchAnimation(QThread):
    def run(self):
        count = 0
        imgList = ["gif/" + x for x in os.listdir("./gif")]
        while True:
            searchWindow.gifImage.setStyleSheet(f"background-image:url({imgList[count]});  background-repeat: no-repeat; background-position: center;")
            count += 1
            count %= len(imgList)
            time.sleep(0.05)



app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
welcomeWindow = welcomeWindow()
insertWindow = insertWindow()
runWindow = runWindow()
searchWindow = searchWindow()
widget.addWidget(welcomeWindow)
widget.addWidget(insertWindow)
widget.addWidget(runWindow)
widget.addWidget(searchWindow)
widget.setFixedHeight(600)
widget.setFixedWidth(950)
widget.setWindowIcon(QIcon("Image/icon.png"))
widget.setWindowTitle("DPIS")
widget.show()
sys.exit(app.exec())
