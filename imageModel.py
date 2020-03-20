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
        self.imgByte = cv.imread(imgPath)
        self.dft = cv.dft(np.float32(self.imgByte),flags = cv.DFT_COMPLEX_OUTPUT)
        self.real = self.dft[0]
        self.imaginary = self.dft[1]
        self.magnitude = None
        self.phase = None
   
    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        """
        a function that takes ImageModel object mag ratio, phase ration 
        """
        ### 
        # implement this function
        ###
        pass