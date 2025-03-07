# Library
import numpy as np
import cv2 as cv

# Ball detection function
# Inspiration from: https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html
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

    # Resizing, blurring and removing the top for better ball detection
    im_RGB = cv.resize(im_RGB, (new_width, new_height))
    im_gray = cv.resize(im_gray, (new_width, new_height))
    im_gray = cv.medianBlur(im_gray, 5)
    im_gray[:new_height // 3, :] = 0

    # Finding the circles in the image
    circles = cv.HoughCircles(im_gray, cv.HOUGH_GRADIENT_ALT, 1, 15, param1 = 30, param2 = 0.8,
                              minRadius = 0, maxRadius = 45)
    circles = np.uint16(np.around(circles))
    
    # Converting to HSV color space
    im_HSV = cv.cvtColor(im_RGB, cv.COLOR_BGR2HSV)
    cirColor = np.zeros((circles.shape[1], 3))

    # Finding out the color of each detected circles
    for idx, val in enumerate(circles[0]):
        # The HSV channels
        H_ch = im_HSV[val[1], val[0], 0]
        S_ch = im_HSV[val[1], val[0], 1]
        V_ch = im_HSV[val[1], val[0], 2]

        # Color argument with 0 for no ball, 1 for red ball, 2 for white ball and 3 for blue ball
        if (H_ch >= 160 or H_ch <= 7) and (S_ch >= 128 and S_ch <= 255) and (V_ch >= 0 and V_ch <= 255):
            cirColor[idx] = np.array([val[1], val[0], 1])
        elif (H_ch >= 0 and H_ch <= 179) and (S_ch >= 0 and S_ch <= 50) and (V_ch >= 92 and V_ch <= 255):
            cirColor[idx] = np.array([val[1], val[0], 2])
        elif (H_ch >= 92 and H_ch <= 127) and (S_ch >= 128 and S_ch <= 255) and (V_ch >= 0 and V_ch <= 255):
            cirColor[idx] = np.array([val[1], val[0], 3])
        else:
            cirColor[idx] = np.array([val[1], val[0], 0])
    
    # Show the image
    if show == True:
        # Place the circles in the RGB image
        for val in circles[0, :]:
            cv.circle(im_RGB, (val[0], val[1]), val[2], (0, 255, 0), 2)
            cv.circle(im_RGB, (val[0], val[1]), 2, (0, 0, 255), 3)
        
        # Show the RGB image with detected circles
        cv.imshow('Detected circles', im_RGB)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Returning the circles
    return cirColor

imagePath = "C:/Users/shaia/Pictures/COCO images/image_data/image48.png"
color = findBall(imagePath, True)
print(color)
