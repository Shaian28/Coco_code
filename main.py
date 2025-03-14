from Robot import Robot

if __name__ == "__main__":
    taskList = ["Boom", "Ramp up", "See saw"]
    robot = Robot(taskList)
    print(robot.Camera.ExternMat)
    #robot.Camera.TakeImage("testImage1.jpg")
    #robot.Camera.TakeImage("testImage2.jpg")