from Robot import Robot

if __name__ == "__main__":
    taskList = ["Boom", "Ramp up", "See saw"]
    robot = Robot(taskList)
    robot.Camera.TakeImage("image1.jpg")