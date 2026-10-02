from machine import Pin, PWM
import time
import math

# 16番から21番まで、計6個のサーボを定義
servo_pins = range(16, 22)
servos = [PWM(Pin(p)) for p in servo_pins]



def map_range(x, in_min, in_max, out_min, out_max):
  return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# 角度をPWMデューティに変換して特定のサーボに送る関数
def set_servo_angle(servo_obj, angle):
    angle = map_range(angle, in_min=0, in_max=180, out_min=10, out_max=180)
    duty = int(1638 + (angle / 180) * (7864 - 1638))
    servo_obj.duty_u16(duty)


time.sleep(0.1)
for s in servos:
    s.freq(50)  # 50Hz

# while True:
#     a=(math.sin(time.ticks_ms()/1000)*45+45+90)
#     # time.sleep(0.01)
#     set_servo_angle(servos[0], 180-a)
#     set_servo_angle(servos[1], a)
#     set_servo_angle(servos[2], 180-a)
#     set_servo_angle(servos[3], a)
#     set_servo_angle(servos[4],180- a)
#     set_servo_angle(servos[5], a)

def servo_set_hex(i,angle):
    if i%2==0:
        angle=180-angle
    set_servo_angle(servos[i], angle)

while True:
    a=(math.sin(time.ticks_ms()/3000)*45+45+90)
    b=(math.sin(time.ticks_ms()/3000)*-45+45+90)
    for i in range(6):
        # servo_set_hex(i, a if i % 2 == 0 else b)
        servo_set_hex(i, a )
        time.sleep(0.1)
    # set_servo_angle(servos[0], 180-a)
    # set_servo_angle(servos[1], a)
    # set_servo_angle(servos[2], 180-a)
    # set_servo_angle(servos[3], a)
    # set_servo_angle(servos[4],180- a)
    # set_servo_angle(servos[5], a)




# for s in servos:
#     set_servo_angle(s, 90)

print("Finished.")