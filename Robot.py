import numpy as np
import subprocess
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
        # Status of the task that should be done during competition
        # with first array element for status of attempt
        # and second array element for points for each task
        self.Task.Status = {"Boom": [0, 1], "Goal": [0, 2], "Ramp up": [0, 1], "Ramp down": [0, 1],
                            "Stairs": [0, 2], "Seesaw": [0, 1], "Golf balls": [0, 2], "3-gate": [0, 1],
                            "Axe": [0, 2], "Luggage delivery": [0, 1], "Ball sorting": [0, 1]}
        # Point gathered in the competition
        self.Task.Point = 0
        # The plan of which task to do in the competition
        self.Task.Plan = masterplan
        # Import the camera class
        self.Camera.Picam = Picamera2()
        # Camera Calibration matrix
        self.Camera.InternMat = np.array([[2.5730e+3, 0, 1.6043e+3],
                                          [0, 2.5786e+3, 1.1901e+3],
                                          [0, 0, 1]])
        self.Camera.ExternMat = np.array([[0, 0, 0, 0],
                                          [0, 0, 0, 0],
                                          [0, 0, 0, 0],
                                          [0, 0, 0, 0]])
        # How much the camera is tilted downward
        self.Camera.Tilt = 0
        # The length of the robot
        self.Dimension.Length = 0
        # The width of the robot
        self.Dimension.Width = 0
        # The heigth of the robot
        self.Dimension.Height = 0
        # The length of the gripper
        self.Dimension.GripLength = 0
        # The height of the camera
        self.Dimension.CameraHeight = 0

    # Funktion for taking an image (not sure if it works)
    def TakeImage(self, filename = "image.jpg"):
        # Run the bash script for capturing images in a new terminal (haven't tested it yet)
        subprocess.run(["gnome-terminal", "--", "bash", "-c", f"./captureImage.sh {filename}; exec bash"])

    # Function for controlling the gripper
    def GripperAction(self):
        # Write a function for the gripper
        return 0