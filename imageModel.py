## This is the abstract class that the students should implement  
import numpy as np
import cv2 as cv
import math
import cmath 
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
        self.dft = np.fft.fft(self.imgByte) 
        self.real = self.dft.real
        self.imaginary = self.dft.imag
        self.magnitude , self.phase = cv.cartToPolar(self.real,self.imaginary,angleInDegrees = True)
        self.uniMagnitude = np.where(self.magnitude>0.5,1,1)
        self.uniPhase = self.phase*0
        self.uniMag = False
        self.uniPhase = False

    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        """
        a function that takes ImageModel object mag ratio, phase ration 
        """
        ### 
        # implement this function
        ###
        if mode.value == 0:
            if (self.uniMag&self.uniPhase):
                mix = (self.uniMagnitude*magnitudeOrRealRatio + imageToBeMixed.magnitude*(1-magnitudeOrRealRatio))*np.exp(self.phase*(1-phaesOrImaginaryRatio)+imageToBeMixed.uniPhase*phaesOrImaginaryRatio)
            elif (self.uniMag):
                mix = (self.uniMagnitude*magnitudeOrRealRatio + imageToBeMixed.magnitude*(1-magnitudeOrRealRatio))*np.exp(self.phase*(1-phaesOrImaginaryRatio)+imageToBeMixed.phase*phaesOrImaginaryRatio)
            elif (self.uniPhase):
                mix = (self.magnitude*magnitudeOrRealRatio + imageToBeMixed.magnitude*(1-magnitudeOrRealRatio))*np.exp(self.phase*(1-phaesOrImaginaryRatio)+imageToBeMixed.uniPhase*phaesOrImaginaryRatio)
            else:
                mix = (self.magnitude*magnitudeOrRealRatio + imageToBeMixed.magnitude*(1-magnitudeOrRealRatio))*np.exp(self.phase*(1-phaesOrImaginaryRatio)+imageToBeMixed.phase*phaesOrImaginaryRatio)
        elif mode.value == 1:
            mix =(self.real*magnitudeOrRealRatio+imageToBeMixed.real*(1-magnitudeOrRealRatio))+ 1j*(self.imaginary*(1-phaesOrImaginaryRatio)+imageToBeMixed.imaginary*phaesOrImaginaryRatio)
        invImg = np.real(np.fft.ifft(mix))
        return invImg