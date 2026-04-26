from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

sensor = robot.getDevice('ds0')
sensor.enable(timestep)

MAX_SPEED = 3.0   # adjust for your robot limits
SLOW_DIST = 0.08  # value where robot starts slowing down (experiment!)

while robot.step(timestep) != -1:
    distance = sensor.getValue()   # This will be between 0 (far) and ~1024 (very close)
    # The lookup table: 0=1024(far), 0.15=0(near). So invert and normalize:
    normalized_distance = (1024 - distance) / 1024  # 1 = no obstacle, 0 = very close
    # Simple proportional speed (tweak factor as needed)
    speed = MAX_SPEED * normalized_distance
    if normalized_distance < 0.1:
        speed = 0  # stop very close!
    left_motor.setVelocity(speed)
    right_motor.setVelocity(speed)
