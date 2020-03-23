import cv2 as cv
from PyQt5 import QtWidgets,QtCore,QtGui
from mainwindow import Ui_MainWindow
from imageModel import ImageModel
from modesEnum import Modes
import itertools
import numpy as np
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: Line No %(lineno)s ::  %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
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
            self.Sliders[i].valueChanged.connect(lambda:self.Output("A Change Has Been Made In The Mixing Ratio Responsible for Module Number " +str(i)+" of Mixing"))
        self.ComponentComboBoxs[0].activated.connect(lambda: self.chooseComp(0))
        self.ComponentComboBoxs[1].activated.connect(lambda: self.chooseComp(1))
        self.ui.ChooseOutput.activated.connect(lambda:self.Output("A Change Has Been Made In The Output Combobox Responsible for The First Module of Mixing"))
        self.ui.ComponentOutput1.activated.connect(lambda:self.Output("A Change Has Been Made In The Component Combobox Responsible for The First Module of Mixing"))
        self.ui.ComponentOutput2.activated.connect(lambda:self.Output("A Change Has Been Made In The Component Combobox Responsible for The Second Module of Mixing"))
        self.ui.ChooseImage1.activated.connect(lambda:self.Output("A Change Has Been Made In The Input Combobox Responsible for The First Module of Mixing"))
        self.ui.ChooseImage2.activated.connect(lambda:self.Output("A Change Has Been Made In The Input Combobox Responsible for The First Module of Mixing"))

    def getFile(self):
        options =  QtWidgets.QFileDialog.Options()
        imgPath = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", "(*.jpg) ;;(*png) ;; (*jpeg);; (*gif) ", options=options) 
        if(imgPath[0]!=''):
            if (self.inputImages[0].pixmap()==None):
                self.inputData[0] = ImageModel(imgPath[0])  
                logger.info('Uploaded The Image With The Path {path} Successfully.'.format(path=imgPath[0]))
                self.showImage(self.inputData[0].imgByte,self.inputImages[0],0)
                self.imageSize = self.inputData[0].imgByte.shape
            elif (self.inputImages[1].pixmap()==None):
                self.inputData[1] = ImageModel(imgPath[0])
                if(self.inputData[1].imgByte.shape == self.imageSize): 
                    logger.info('Uploaded The Image With The Path {path} Successfully.'.format(path=imgPath[0]))
                    self.showImage(self.inputData[1].imgByte,self.inputImages[1],1)    
                else:
                    logger.warning('Shape Of Image 2 Does Not Match Shape Of Image 1.')

    def showImage(self,image,component,index):
        cv.imwrite("results/edit.jpg", np.float64(image)) 
        pixmap = QtGui.QPixmap('results/edit.jpg')
        component.setPixmap(pixmap)
        component.setScaledContents(True)
        logger.info('Displayed The Image Successfully')

    def chooseComp(self,index):
        if(self.inputData[index]):
            logger.info('The Combobox Responsible for Image Number {i} Has Been Changed to {text}.'.format(i=index+1,text= str(self.ComponentComboBoxs[index].currentText())))
            if (str(self.ComponentComboBoxs[index].currentText())=="FT Magnitude Component"):
                self.showImage(self.inputData[index].magnitude,self.FTImages[index],index)
            elif (str(self.ComponentComboBoxs[index].currentText())=="FT Phase Component"):
                self.showImage(self.inputData[index].phase,self.FTImages[index],index)
            elif (str(self.ComponentComboBoxs[index].currentText())=="FT Real Component"):
                self.showImage(self.inputData[index].real,self.FTImages[index],index)
            elif (str(self.ComponentComboBoxs[index].currentText())=="FT Imaginary Component"):
                self.showImage(self.inputData[index].imaginary,self.FTImages[index],index)
        else:
                logger.warning('The Combobox Responsible for image number {i} Has Been Changed but There is no Image in This Module.'.format(i=index+1))

    def Output(self,message):
        if(self.inputData[0] and self.inputData[1]):
            logger.info('{message}.'.format(message=message))
            outputIndex = self.ui.ChooseOutput.currentIndex()
            imageIndex = [self.ui.ChooseImage1.currentIndex(),self.ui.ChooseImage2.currentIndex()]
            mixingRatio = [self.ui.MixingRatio1.value()/100,self.ui.MixingRatio2.value()/100]
            percentage = [self.ui.Percentage1,self.ui.Percentage2]
            compIndex = [self.ui.ComponentOutput1.currentIndex(),self.ui.ComponentOutput2.currentIndex()]
            for i in range(len(imageIndex)):
                percentage[i].setText(str(mixingRatio[i]*100)+"%")
                modeIndex = "testMagAndPhaseMode" if compIndex[i] in (0,1,4,5) else "testRealAndImagMode"                    
                if compIndex[i] in(0,2,4):
                    self.inputData[imageIndex[i]].uniMag = True if compIndex[i] == 4 else False
                    self.inputData[imageIndex[abs(i-1)]].uniMag = True if compIndex[abs(i-1)] == 4 else False
                    self.outputData[outputIndex]= self.inputData[imageIndex[i]].mix(self.inputData[imageIndex[abs(i-1)]],mixingRatio[i],mixingRatio[abs(i-1)],Modes(modeIndex))
                    self.ChangeCombobox(compIndex[0])
                else:
                    self.inputData[imageIndex[i]].uniPhase = True if compIndex[i]==5 else False
                    self.inputData[imageIndex[abs(i-1)]].uniPhase = True if compIndex[abs(i-1)] == 4 else False
                    self.outputData[outputIndex] = self.inputData[imageIndex[abs(i-1)]].mix(self.inputData[imageIndex[i]],mixingRatio[abs(i-1)],mixingRatio[i],Modes(modeIndex))
                    self.ChangeCombobox(compIndex[0])
            logger.info('The Mixing Has Been Done Successfully')
            self.showImage(self.outputData[outputIndex],self.OutputImages[outputIndex],outputIndex)
        else:
            logger.warning('{message}, but The Application Does not Have to Images Uploaded to it.'.format(message=message))

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
            self.ui.ComponentOutput2.view().setRowHidden(i,False)
            self.ui.ComponentOutput2.view().setRowHidden(j,True)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow() 
    window.show()
    sys.exit(app.exec_())