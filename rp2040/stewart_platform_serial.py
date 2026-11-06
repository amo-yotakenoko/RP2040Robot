from machine import Pin, PWM, I2C
import sys
import select
import ssd1306
import time
import _thread
from servo import Servo, servo_loop


# OLEDディスプレイの初期化
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
display = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)






    

# サーボの初期化 (16〜21番)
servos = [Servo(p) for p in range(16, 22)]




# シリアル入力の監視準備
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)



display.fill(0)
display.rotate(False)
# for i ,m in enumerate(["20261018"]):
#     display.text(m, 0, i*16, 1)

display.show()


_thread.start_new_thread(servo_loop, (servos,))

for i,servo in enumerate(servos):
    time.sleep(0.1)  
    servo.set_servo_angle(90)
    display.fill(0)
    display.text(f"{'#'*(i+1)}{'_'*(5-i)}", 0, 0, 1)
    display.show()
display.text(f"OK!", 0, 16, 1)

display.show()


# サーボスレッド起動（以後 update() はメインループで呼ばない）
# for j in range(45):
#         time.sleep(0.1)

last_disp = time.ticks_ms()

while True:
    # display.fill(0)
    # display.text(f"{time.ticks_ms()}", 0, 0, 1)
    # シリアルからデータが来ていれば非ブロッキングで読み取る
    # （溜まった分はまとめて捌いて古い指令の遅延を防ぐ）
    while poll.poll(0):
        line = sys.stdin.readline()
        if not line:
            break
        current_msg = line.strip()
        display.text(f"{current_msg}", 0, 16, 1)
        display.show()

        # 「0,90」のような形式であればサーボを動かす
        try:
            if ',' in current_msg:
                parts = current_msg.split(',')
                if len(parts) == 2:
                    if parts[0] == "FACE":
                        image_data = bytes.fromhex(parts[1])
                        display.buffer[:] = image_data
                        display.show()
                    else:
                        ch = int(parts[0])
                        angle = float(parts[1])
                        if 0 <= ch < len(servos):
                            servos[ch].set_servo_angle(angle)
        except:
            pass
    # display.show()


   

    # GILを譲ってサーボスレッドを回す
    time.sleep_ms(1)

