from machine import Pin, PWM, I2C
from servo import Servo, servo_loop
import _thread
import time

headservos = [Servo(p) for p in range(16, 22)]
servos = [Servo(p) for p in range(22, 28)]

_thread.start_new_thread(servo_loop, (headservos+servos,))


servos[0].set_servo_angle(90)
servos[1].set_servo_angle(90)
servos[2].set_servo_angle(90)
servos[3].set_servo_angle(90)
servos[4].set_servo_angle(90)
servos[5].set_servo_angle(90)
time.sleep(3)

print(0)
servos[0].set_servo_angle(90+45)
time.sleep(1)
servos[0].set_servo_angle(90)
time.sleep(1)

print(1)
servos[1].set_servo_angle(90+45)
time.sleep(1)
servos[1].set_servo_angle(90)


print(2)
servos[2].set_servo_angle(90+45)
time.sleep(1)
servos[2].set_servo_angle(90)

print(3)
servos[3].set_servo_angle(90+45)
time.sleep(1)
servos[3].set_servo_angle(90)

print(4)
servos[4].set_servo_angle(90+45)
time.sleep(1)
servos[4].set_servo_angle(90)


print(5)
servos[5].set_servo_angle(90+45)
time.sleep(1)
servos[5].set_servo_angle(90)

# servos[0].set_servo_angle(90+45)
# time.sleep(1)
# servos[0].set_servo_angle(90)
# time.sleep(1)


# servos[1].set_servo_angle(90)
# # servos[2].set_servo_angle(00)
# # # time.sleep(1)
# # servos[2].set_servo_angle(90)


# # servos[1].set_servo_angle(0)
# # servos[2].set_servo_angle(0)

# servos[3].set_servo_angle(90)
# time.sleep(1)
# servos[3].set_servo_angle(0)
while True:
    time.sleep(1)

    # servos[0].set_servo_angle(90)
