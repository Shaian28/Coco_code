# Library
import numpy as np
import subprocess
import os
from picamera2 import Picamera2

class Robot:
    def __init__(self, masterplan):
        # Name of the robot
        self.Name = "Coco"
        # The language the robot has to learn provided by Duolingo
        self.Language = "Japanese"
        # Relative position given as x, y, z, theta
        self.Position = (0, 0, 0, 0)
        # Number of balls stored
        self.Stored = 0
        # Giving the arguments to Task subclass
        self.Task = self.Task(masterplan)
    
    class Task:
        def __init__(self, masterplan):
            # Status of the task that should be done during competition
            # with first array element for status of attempt
            # and second array element for points for each task
            self.Status = {"Boom": [0, 1], "Goal": [0, 2], "Ramp up": [0, 1], "Ramp down": [0, 1],
                                "Stairs": [0, 2], "Seesaw": [0, 1], "Golf balls": [0, 2], "3-gate": [0, 1],
                                "Axe": [0, 2], "Luggage delivery": [0, 1], "Ball sorting": [0, 1]}
            # Point gathered in the competition
            self.Point = 0
            # The plan of which task to do in the competition
            self.Plan = masterplan

    class Camera:
        def __init__(self):
            # Import the camera class
            self.Picam = Picamera2()
            # Calibration parameters
            self.FocalLengthX = 2.5730e+3
            self.FocalLengthY = 2.5786e+3
            self.CenterX = 1.6043e+3
            self.CenterY = 1.1901e+3
            # Internal (Camera Calibration) matrix
            self.InternMat = np.array([[self.FocalLengthX, 0, self.CenterX],
                                       [0, self.FocalLengthY, self.CenterY],
                                       [0, 0, 1]])
            # External matrix
            self.ExternMat = np.array([[0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 0]])
            # How much the camera is tilted downward
            self.Tilt = 11 * np.pi / 180
        
        # Funtion for taking an image
        def TakeImage(self, filename = "image.jpg"):
            # Run the bash script for capturing images in the background
            subprocess.Popen(f"nohup ./captureImage.sh {filename} > /dev/null 2>&1 &", shell=True)

    class Dimension:
        def __init__(self):
            # The length of the robot
            self.Length = 0
            # The width of the robot
            self.Width = 0
            # The heigth of the robot
            self.Height = 0
            # The length of the gripper
            self.GripLength = 0
            # The height of the camera
            self.CameraHeight = 0
        
    # Function for controlling the gripper
    def GripperAction(self):
        # Write a function for the gripper
        return 0