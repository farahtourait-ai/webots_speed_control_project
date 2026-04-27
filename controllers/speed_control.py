from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# Sensor
front_sensor = robot.getDevice('ds_front')
front_sensor.enable(timestep)

# Parameters
MAX_SPEED = 2.0
SAFE_DISTANCE = 800
STOP_DISTANCE = 300

print("=" * 50)
print(" SPEED CONTROL ROBOT ACTIVE ")
print("=" * 50)

while robot.step(timestep) != -1:
    front_value = front_sensor.getValue()

    # Speed control logic
    if front_value <= STOP_DISTANCE:
        speed = 0.0
        status = "STOPPED"
    elif front_value >= SAFE_DISTANCE:
        speed = MAX_SPEED
        status = "FULL SPEED"
    else:
        speed = MAX_SPEED * (front_value - STOP_DISTANCE) / (SAFE_DISTANCE - STOP_DISTANCE)
        status = "SLOWING DOWN"

    left_motor.setVelocity(speed)
    right_motor.setVelocity(speed)

    print(f"Sensor: {front_value:.2f} | Speed: {speed:.2f} | {status}")
