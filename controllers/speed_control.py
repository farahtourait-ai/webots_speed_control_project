from controller import Robot

# Initialize robot
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Get motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# Get distance sensors
front_sensor = robot.getDevice('ds_front')
left_sensor = robot.getDevice('ds_left')
right_sensor = robot.getDevice('ds_right')

# Enable sensors
front_sensor.enable(timestep)
left_sensor.enable(timestep)
right_sensor.enable(timestep)

# Speed control parameters
MAX_SPEED = 2.0        # Maximum speed in m/s
SAFE_DISTANCE = 500    # Sensor value at 0.8 meters (start slowing)
STOP_DISTANCE = 500    # Sensor value at 0.25 meters (full stop)

print("=== SPEED CONTROL ROBOT STARTED ===")
print("MAX_SPEED: 2.0 m/s")
print("SAFE_DISTANCE: 0.8 m")
print("STOP_DISTANCE: 0.25 m")
print("===================================")

# Main control loop
while robot.step(timestep) != -1:
    # Read front sensor value (higher = farther)
    front_value = front_sensor.getValue()
    
    # Convert sensor value to approximate distance in meters
    if front_value > 0:
        distance = front_value / 1000.0
    else:
        distance = 1.0
    
    # PROPORTIONAL SPEED CONTROL
    if front_value <= STOP_DISTANCE:
        linear_speed = 0.0
        status = "STOPPED"
    elif front_value >= SAFE_DISTANCE:
        linear_speed = MAX_SPEED
        status = "FULL SPEED"
    else:
        # Linear interpolation between STOP and SAFE
        linear_speed = MAX_SPEED * (front_value - STOP_DISTANCE) / (SAFE_DISTANCE - STOP_DISTANCE)
        linear_speed = max(0.0, min(MAX_SPEED, linear_speed))
        status = "SLOWING"
    
    # Simple obstacle avoidance (turn when very close)
    left_value = left_sensor.getValue()
    right_value = right_sensor.getValue()
    
    if front_value < 400 and linear_speed < 0.5:
        # Turn away from the closest obstacle
        if left_value > right_value:
            # Left side more open -> turn right
            left_speed = linear_speed - 0.8
            right_speed = linear_speed + 0.8
            status = "TURNING RIGHT"
        else:
            # Right side more open -> turn left
            left_speed = linear_speed + 0.8
            right_speed = linear_speed - 0.8
            status = "TURNING LEFT"
    else:
        # Go straight
        left_speed = linear_speed
        right_speed = linear_speed
    
    # Apply speeds to motors
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
    
    # Print to console for screenshots
    print("Distance: {:.2f}m | Speed: {:.2f} | {}".format(distance, linear_speed, status))
