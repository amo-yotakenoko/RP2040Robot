from machine import Pin, PWM, I2C
from servo import Servo, servo_loop
import _thread
import time
import math

# headservos = [Servo(p) for p in range(16, 22)]
# servos = [Servo(p) for p in range(22, 28)]
servos = [Servo(p) for p in [22,23,24,12,13,11]]

_thread.start_new_thread(servo_loop, (servos,))


servos[0].set_servo_angle(90)
servos[1].set_servo_angle(90)
servos[2].set_servo_angle(90)
# servos[3].set_servo_angle(90)
# servos[4].set_servo_angle(90)
# servos[5].set_servo_angle(90)
# time.sleep(3)
# while True:
#     for i in range(0, len(servos)):
#         servos[i].set_servo_angle(math.sin(time.ticks_ms()/1000)*90+90)
#     servos[5].set_servo_angle(math.sin(time.ticks_ms()/1000)*90+90)


# for i in range(0, 6):
#     servos[i].set_servo_angle(0)
#     time.sleep(1)
#     servos[i].set_servo_angle(90)
#     time.sleep(1)

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
