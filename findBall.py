# Library
import numpy as np
import cv2 as cv
from Robot import Robot

# Ball detection function
def findBall(path, show = False):
    # Getting the image as RGB and grayscale
    im_RGB = cv.imread(path)
    im_gray = cv.cvtColor(im_RGB, cv.COLOR_BGR2GRAY)

    # Adjusting the scale, so the full frame is in the image
    screen_width = 800
    screen_height = 600
    height, width = im_gray.shape[:2]
    scale_factor = min(screen_width / width, screen_height / height)
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Preprocessing for ball detection
    im_RGB = cv.resize(im_RGB, (new_width, new_height))
    im_gray = cv.resize(im_gray, (new_width, new_height))
    im_gray = cv.medianBlur(im_gray, 5)
    kernel = np.ones((5, 5), np.uint8)
    im_gray = cv.morphologyEx(im_gray, cv.MORPH_CLOSE, kernel)
    im_gray = cv.morphologyEx(im_gray, cv.MORPH_GRADIENT, kernel)
    im_gray[:new_height * 3 // 8, :] = 0

    # Finding the circles in the image
    circles = cv.HoughCircles(im_gray, cv.HOUGH_GRADIENT_ALT, 1, 15, param1 = 50, param2 = 0.8,
                              minRadius = 0, maxRadius = 45)
    circles = np.uint16(np.around(circles))

    # Converting to HSV color space
    im_HSV = cv.cvtColor(im_RGB, cv.COLOR_BGR2HSV)
    detectCircle = []

    # Finding out the color of each detected circles
    for val in circles[0]:
        # The HSV channels
        H_ch = im_HSV[val[1], val[0], 0]
        S_ch = im_HSV[val[1], val[0], 1]
        V_ch = im_HSV[val[1], val[0], 2]

        # Color argument with 1 for red ball, 2 for white ball and 3 for blue ball
        if (H_ch >= 160 or H_ch <= 7) and (S_ch >= 53 and S_ch <= 255) and (V_ch >= 0 and V_ch <= 255):
            detectCircle.append(np.array([val[0], val[1], val[2], 1]))
        elif (H_ch >= 0 and H_ch <= 179) and (S_ch >= 0 and S_ch <= 50) and (V_ch >= 92 and V_ch <= 255):
            detectCircle.append(np.array([val[0], val[1], val[2], 2]))
        elif (H_ch >= 92 and H_ch <= 127) and (S_ch >= 53 and S_ch <= 255) and (V_ch >= 0 and V_ch <= 255):
            detectCircle.append(np.array([val[0], val[1], val[2], 3]))
        else:
            continue
    detectCircle = np.array(detectCircle)
    
    # Show the image
    if show == True:
        # Place the circles in the RGB image
        for val in detectCircle:
            cv.circle(im_RGB, (val[0], val[1]), val[2],
                      (255, 0, 0) if val[3] == 3 else (255, 255, 255) if val[3] == 2 else (0, 0, 255), 2)
            cv.circle(im_RGB, (val[0], val[1]), 2, (0, 0, 255), 3)
        
        # Show the RGB image with detected circles
        cv.imshow('Detected circles', im_RGB)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Returning the circles
    return detectCircle

# Finding the 3D coordinate of the balls
def place3D(circles, robotClass):
    # The pixel, camera and world coordinates initialisation
    pixelPlace = np.array([circles[:, 0], circles[:, 1], np.ones(circles[:, 0].shape)])
    cameraPlace = np.ones((4, pixelPlace.shape[1]))
    worldPlace = np.ones((4, pixelPlace.shape[1]))

    # Looping through all the points
    for idx, point in enumerate(np.transpose(pixelPlace)):
        # Depth information of the detected balls
        depth = 1                                           # Find a way to calculate it

        # Calculation of the camera coordinates
        cameraPlace[0:-1, idx] = np.dot(np.linalg.inv(robotClass.Camera.InternMat), point) * depth
        #cameraPlace[[0, 2], idx] = cameraPlace[[2, 0], idx]            # The coordinates axes was switched in the old assignment
        #cameraPlace[3, idx] = -cameraPlace[3, idx]                     # Have to test the coordinate axis in real-time

        # Calculation of the world coordinates
        worldPlace[:, idx] = np.dot(robotClass.Camera.ExternMat, cameraPlace[:, idx])
        worldPlace[:, idx] = worldPlace[:, idx] / worldPlace[-1, idx]
    
    # Return world coordinates
    return worldPlace

# Debugging
if __name__ == "__main__":
    taskList = ["Golf balls", "Ball sorting"]
    robot = Robot(taskList)
    imagePath = "C:/Users/shaia/Pictures/COCO images/image_data/"
    imageFile = ["image12.png", "image13.png", "image14.png", "image46.png", "image47.png", "image48.png"]
    color = findBall(imagePath + imageFile[4])
    place3D(color, robot)
