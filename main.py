from PyQt5 import QtWidgets,QtCore,QtGui
from mainwindow import Ui_MainWindow
import cv2 as cv
from imageModel import ImageModel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Upload.triggered.connect(self.getFile)
        self.imageData=[None]*2
        self.inputImages = [self.ui.InputImage1,self.ui.InputImage2]
        self.FTImages = [self.ui.FT_Image1,self.ui.FT_Image2]
        self.OutputImages = [self.ui.OutputImage1,self.ui.OutputImage2]
        self.ComponentComboBoxs = [self.ui.ComponentInput1,self.ui.ComponentInput2]
        self.ui.ComponentInput1.activated.connect(lambda: self.chooseComp(0))
        for i in range (len(self.ComponentComboBoxs)):
            self.ComponentComboBoxs[i].activated.connect(lambda: self.chooseComp(i))

    def getFile(self):
        options =  QtWidgets.QFileDialog.Options()
        imgPath = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", "(*.jpg) ;;(*png) ;; (*jpeg) ", options=options) 
        if(imgPath[0]!=''):
            if (self.inputImages[0].pixmap()==None):
                self.imageData[0] = ImageModel(imgPath[0])  
                self.showImage(self.imageData[0].imgByte,0)
            elif (self.inputImages[1].pixmap()==None):
                self.imageData[1] = ImageModel(imgPath[0])  
                self.showImage(self.imageData[1].imgByte,1)               
            else:
                pass
        else:
            pass 

    def showImage(self,image,index):
        cv.imwrite("image.jpeg", image) 
        pixmap = QtGui.QPixmap('image.jpeg')
        self.inputImages[index].setPixmap(pixmap)
        self.inputImages[index].setScaledContents(True)
        self.inputImages[index].setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.FTImages[index].setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.OutputImages[0].setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        self.OutputImages[1].setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)



       

    # def showInput(self,image,index):
    #     image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
    #     self.inputImages[index].setPixmap(QtGui.QPixmap.fromImage(image))
    #     self.inputImages[index].setScaledContents(True)
    #     self.inputImages[index].setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
    #     self.FTImages[index].setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
    #     self.OutputImages[index].setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)

    def displayFFT(self,component,index):
        cv.imwrite("fft.jpeg", component) 
        pixmap = QtGui.QPixmap('fft.jpeg')
        self.FTImages[index].setPixmap(pixmap)
        self.FTImages[index].setScaledContents(True)


    # def displayFFT(self,component,index):
    #     image = QImage(component.data, component.shape[1], component.shape[0], QImage.Format_Grayscale8)
    #     self.FTImages[index].setPixmap(QtGui.QPixmap.fromImage(image))
    #     self.FTImages[index].setScaledContents(True)

    def chooseComp(self,index):
        if(self.imageData[index]):
            if (str(self.ComponentComboBoxs[index].currentText())=="FT Magnitude"):
                self.displayFFT(self.imageData[index].magnitude,index)
            elif (str(self.ComponentComboBoxs[index].currentText())=="FT Phase"):
                self.displayFFT(self.imageData[index].phase,index)
            elif (str(self.ComponentComboBoxs[index].currentText())=="FT Real component"):
                self.displayFFT(self.imageData[index].real,index)
            elif (str(self.ComponentComboBoxs[index].currentText())=="FT Imaginary component"):
                self.displayFFT(self.imageData[index].imaginary,index)
            else:
                pass



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow() 
    window.show()
    sys.exit(app.exec_())