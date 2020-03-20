from PyQt5 import QtWidgets,QtCore,QtGui
from mainwindow import Ui_MainWindow
from imageModel import ImageModel

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Upload.clicked.connect(self.getFile)


    def getFile(self):
        options =  QtWidgets.QFileDialog.Options()
        imgPath = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", "(*.jpg) ;;(*png) ", options=options) 
        if(imgPath[0]!=''):
            image = ImageModel(imgPath)
        else:
            pass               


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow() 
    window.show()
    sys.exit(app.exec_())