import cv2 as cv
from PyQt5 import QtWidgets,QtCore,QtGui
from mainwindow import Ui_MainWindow
from imageModel import ImageModel
from modesEnum import Modes
import itertools

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Upload.triggered.connect(self.getFile)
        self.inputData=[None]*2
        self.outputData=[None]*2
        self.inputImages = [self.ui.InputImage1,self.ui.InputImage2]
        self.FTImages = [self.ui.FT_Image1,self.ui.FT_Image2]
        self.OutputImages = [self.ui.OutputImage1,self.ui.OutputImage2]
        self.ComponentComboBoxs = [self.ui.ComponentInput1,self.ui.ComponentInput2]
        self.Sliders = [self.ui.MixingRatio1,self.ui.MixingRatio2]
        self.realTime()

    def realTime(self):
        for i in range(len(self.Sliders)):
            self.Sliders[i].valueChanged.connect(self.Output)
        self.ComponentComboBoxs[0].activated.connect(lambda: self.chooseComp(0))
        self.ComponentComboBoxs[1].activated.connect(lambda: self.chooseComp(1))
        self.ui.ChooseOutput.activated.connect(self.Output)
        self.ui.ComponentOutput1.activated.connect(self.Output)
        self.ui.ComponentOutput2.activated.connect(self.Output)
        self.ui.ChooseImage1.activated.connect(self.Output)
        self.ui.ChooseImage2.activated.connect(self.Output)

    def getFile(self):
        options =  QtWidgets.QFileDialog.Options()
        imgPath = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", "(*.jpg) ;;(*png) ;; (*jpeg) ", options=options) 
        if(imgPath[0]!=''):
            if (self.inputImages[0].pixmap()==None):
                self.inputData[0] = ImageModel(imgPath[0])  
                self.showImage(self.inputData[0].imgByte,self.inputImages[0],0)
                self.imageSize = self.inputData[0].imgByte.shape
            elif (self.inputImages[1].pixmap()==None):
                self.inputData[1] = ImageModel(imgPath[0])
                if(self.inputData[1].imgByte.shape == self.imageSize):  
                    self.showImage(self.inputData[1].imgByte,self.inputImages[1],1)     
   
    def showImage(self,image,component,index):
        cv.imwrite("results/edit.jpg", image) 
        pixmap = QtGui.QPixmap('results/edit.jpg')
        component.setPixmap(pixmap)
        component.setScaledContents(True)

    def chooseComp(self,index):
        if(self.inputData[index]):
            if (str(self.ComponentComboBoxs[index].currentText())=="FT Magnitude"):
                self.showImage(self.inputData[index].magnitude,self.FTImages[index],index)
            elif (str(self.ComponentComboBoxs[index].currentText())=="FT Phase"):
                self.showImage(self.inputData[index].phase,self.FTImages[index],index)
            elif (str(self.ComponentComboBoxs[index].currentText())=="FT Real component"):
                self.showImage(self.inputData[index].real,self.FTImages[index],index)
            elif (str(self.ComponentComboBoxs[index].currentText())=="FT Imaginary component"):
                self.showImage(self.inputData[index].imaginary,self.FTImages[index],index)
            else:
                pass

    def Output(self):
        if(self.inputData[0] and self.inputData[1]):
            outputIndex = self.ui.ChooseOutput.currentIndex()
            imageIndex = [self.ui.ChooseImage1.currentIndex(),self.ui.ChooseImage2.currentIndex()]
            mixingRatio = [self.ui.MixingRatio1.value()/100,self.ui.MixingRatio2.value()/100]
            percentage = [self.ui.Percentage1,self.ui.Percentage2]
            compIndex = [self.ui.ComponentOutput1.currentIndex(),self.ui.ComponentOutput2.currentIndex()]
            for i in range(len(imageIndex)):
                percentage[i].setText(str(mixingRatio[i]*100)+"%")
                modeIndex = 0 if compIndex[imageIndex[i]] in (0,1,4,5) else 1                    
                if compIndex[imageIndex[i]] in(0,2,4):
                    self.inputData[imageIndex[i]].uniMag = True if compIndex[imageIndex[i]] == 4 else False
                    self.outputData[outputIndex]= self.inputData[imageIndex[i]].mix(self.inputData[abs(imageIndex[i]-1)],mixingRatio[imageIndex[i]],mixingRatio[abs(imageIndex[i]-1)],Modes(modeIndex))
                    self.ChangeCombobox(compIndex[0])
                else:
                    self.inputData[imageIndex[i]].uniPhase = True if compIndex[imageIndex[i]]==5 else False
                    self.outputData[outputIndex] = self.inputData[abs(imageIndex[i]-1)].mix(self.inputData[imageIndex[i]],mixingRatio[abs(imageIndex[i]-1)],mixingRatio[imageIndex[i]],Modes(modeIndex))
                    self.ChangeCombobox(compIndex[0])
            self.showImage(self.outputData[outputIndex],self.OutputImages[outputIndex],outputIndex)

    def ChangeCombobox(self,choosenIndex):
        if choosenIndex in (0, 4):
            visibleElements,hiddenElements = [1,5],[0,2,3,4]
        elif choosenIndex in (1,5):
            visibleElements,hiddenElements = [0,4],[1,2,3,5]  
        elif choosenIndex == 2:
            visibleElements,hiddenElements = [3],[0,1,2,4,5]
        else:
            visibleElements,hiddenElements = [2], [0,1,3,4,5]
        for i,j in itertools.product(visibleElements,hiddenElements):
            self.ui.ComponentOutput2.model().item(i).setEnabled(True)
            self.ui.ComponentOutput2.model().item(j).setEnabled(False)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow() 
    window.show()
    sys.exit(app.exec_())