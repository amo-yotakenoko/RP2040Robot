from machine import Pin, PWM, I2C
import _thread
import time


# サーボ目標値の共有用ロック（メインスレッド⇔サーボスレッド間）
servo_lock = _thread.allocate_lock()

class Servo:
    def __init__(self, pin_number):
        self.pwm = PWM(Pin(pin_number))
        self.pwm.freq(50)  # 50Hz for standard servos
        self.now_angle = 90.0
        self.target_angle = 90.0
        self.enable = False
        self.update()
        self.last_update_time = time.ticks_ms()

    def set_servo_angle(self, target_angle):
        servo_lock.acquire()
        try:
            self.target_angle = float(target_angle)
            if not self.enable:
                self.pwm.init()
                self.pwm.freq(50)
                self.last_update_time = time.ticks_ms()
            self.enable = True
        finally:
            servo_lock.release()

    def get_angle(self):
        servo_lock.acquire()
        try:
            return self.now_angle
        finally:
            servo_lock.release()

    def update(self):
        if not self.enable:
            return
        # サーボスレッドからのみ呼ぶ。ロックは短時間だけ掴む。
        servo_lock.acquire()
        try:
            target = self.target_angle
            now = self.now_angle
        finally:
            servo_lock.release()

        delta = (target - now) * 0.02
        delta = max(-0.1, min(0.1, delta))
        now += delta
        
        # 残差が微小なら吸着させて int 切り捨て停滞を防ぐ
        if abs(target - now) < 0.05:
            now = target
        else:
            self.last_update_time = time.ticks_ms()


            # self.pwm.duty_u16(0)
            # self.pwm.deinit()
            # print("Servo reached target angle:", now)

        servo_lock.acquire()
        try:
            self.now_angle = now
        finally:
            servo_lock.release()

        duty_min=1638
        duty_max=8192
        mapped_margin=0

        # #ASV-15-Aの場合
        # duty_max=7864 
        # mapped_margin=10

        # マッピングしてduty_u16に変換
        mapped = int(now * (180 - 10) / 180 + 10)
        duty = int(duty_min + (mapped / 180) * (duty_max - duty_min))

        if( time.ticks_ms() < self.last_update_time + 1000 ):
            self.pwm.duty_u16(duty)
        else:
            self.pwm.duty_u16(0)
            self.pwm.deinit()
            servo_lock.acquire()
            try:
                self.enable = False
            finally:
                servo_lock.release()
            print("サーボ無効化")



def servo_loop(servos):

    while True:
        for servo in servos:
            servo.update()
        time.sleep(0.0001)
