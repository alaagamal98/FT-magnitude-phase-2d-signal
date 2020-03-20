## This is the abstract class that the students should implement  
import numpy as np
import cv2 as cv
import math
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
        self.imgByte = cv.imread(imgPath,cv.IMREAD_COLOR)
        self.dft = np.fft.fft(self.imgByte) 
        self.real = self.dft.real.astype(int)
        self.imaginary = self.dft.imag.astype(int)
        self.invImg = np.real(np.fft.ifft(self.dft)).astype(int)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(self.dft)


    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        """
        a function that takes ImageModel object mag ratio, phase ration 
        """
        ### 
        # implement this function
        ###
        pass