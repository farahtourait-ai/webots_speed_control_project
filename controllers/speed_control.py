from controller import Robot
robot = Robot()
print("Controller started")
while robot.step(int(robot.getBasicTimeStep())) != -1:
    pass
