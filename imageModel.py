## This is the abstract class that the students should implement  
import numpy as np
import cv2 as cv
from modesEnum import Modes

class ImageModel():

    """
    A class that represents the ImageModel"
    """

    def __init__(self):
        pass

    def __init__(self, imgPath: str):
        self.imgPath = imgPath
        ###
        # ALL the following properties should be assigned correctly after reading imgPath  
        ###
        self.imgByte = cv.imread(imgPath,cv.IMREAD_GRAYSCALE)
        self.dft = cv.dft(np.float64(self.imgByte),flags = cv.DFT_COMPLEX_OUTPUT)
        self.real= self.dft[:,:,0]
        self.imaginary = self.dft[:,:,1]
        self.magnitude , self.phase = cv.cartToPolar(self.real,self.imaginary,angleInDegrees= True)
        self.uniMagnitude = np.ones(self.magnitude.shape)
        self.uniPhase = np.zeros(self.phase.shape)
        self.uniMag = False
        self.uniPh = False

    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        """
        a function that takes ImageModel object mag ratio, phase ration 
        """
        ### 
        # implement this function
        ###
        mix = np.zeros((self.imgByte.shape[0],self.imgByte.shape[1],2),'float64')
        if mode.value == "testMagAndPhaseMode":
            if (self.uniMag and imageToBeMixed.uniPh):
                real,imaginary = cv.polarToCart(self.uniMagnitude*magnitudeOrRealRatio + imageToBeMixed.magnitude*(1-magnitudeOrRealRatio),self.phase* (1-phaesOrImaginaryRatio)+imageToBeMixed.uniPhase* phaesOrImaginaryRatio,angleInDegrees=  True )
            elif (self.uniMag):
                real,imaginary  = cv.polarToCart(self.uniMagnitude*magnitudeOrRealRatio + imageToBeMixed.magnitude*(1-magnitudeOrRealRatio),self.phase* (1-phaesOrImaginaryRatio)+imageToBeMixed.phase* phaesOrImaginaryRatio,angleInDegrees=  True )
            elif (imageToBeMixed.uniPh):
                real,imaginary  = cv.polarToCart(self.magnitude*magnitudeOrRealRatio + imageToBeMixed.magnitude*(1-magnitudeOrRealRatio),self.phase* (1-phaesOrImaginaryRatio)+imageToBeMixed.uniPhase* phaesOrImaginaryRatio ,angleInDegrees=  True)
            else:
                real,imaginary  = cv.polarToCart(self.magnitude*magnitudeOrRealRatio + imageToBeMixed.magnitude*(1-magnitudeOrRealRatio),self.phase* (1-phaesOrImaginaryRatio)+imageToBeMixed.phase* phaesOrImaginaryRatio,angleInDegrees=  True )
        elif mode.value == "testRealAndImagMode":
            real = self.real*magnitudeOrRealRatio+imageToBeMixed.real*(1-magnitudeOrRealRatio)
            imaginary = self.imaginary* (1-phaesOrImaginaryRatio)+imageToBeMixed.imaginary* phaesOrImaginaryRatio
        mix[:,:,0] , mix[:,:,1] =  real, imaginary
        invImg = cv.idft(mix,flags=cv.DFT_SCALE | cv.DFT_REAL_OUTPUT)
        invImg *= 255.0/np.max(invImg)
        return invImg