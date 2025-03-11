# Library
import numpy as np
import cv2 as cv

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
    cirColor = []

    # Finding out the color of each detected circles
    for val in circles[0]:
        # The HSV channels
        H_ch = im_HSV[val[1], val[0], 0]
        S_ch = im_HSV[val[1], val[0], 1]
        V_ch = im_HSV[val[1], val[0], 2]

        # Color argument with 1 for red ball, 2 for white ball and 3 for blue ball
        if (H_ch >= 160 or H_ch <= 7) and (S_ch >= 53 and S_ch <= 255) and (V_ch >= 0 and V_ch <= 255):
            cirColor.append(np.array([val[1], val[0], val[2], 1]))
        elif (H_ch >= 0 and H_ch <= 179) and (S_ch >= 0 and S_ch <= 50) and (V_ch >= 92 and V_ch <= 255):
            cirColor.append(np.array([val[1], val[0], val[2], 2]))
        elif (H_ch >= 92 and H_ch <= 127) and (S_ch >= 53 and S_ch <= 255) and (V_ch >= 0 and V_ch <= 255):
            cirColor.append(np.array([val[1], val[0], val[2], 3]))
        else:
            continue
    cirColor = np.array(cirColor)
    
    # Show the image
    if show == True:
        # Place the circles in the RGB image
        for val in cirColor:
            cv.circle(im_RGB, (val[1], val[0]), val[2],
                      (255, 0, 0) if val[3] == 3 else (255, 255, 255) if val[3] == 2 else (0, 0, 255), 2)
            cv.circle(im_RGB, (val[1], val[0]), 2, (0, 0, 255), 3)
        
        # Show the RGB image with detected circles
        cv.imshow('Detected circles', im_RGB)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Returning the circles
    return cirColor

imagePath = "C:/Users/shaia/Pictures/COCO images/image_data/image48.png"
color = findBall(imagePath, True)
