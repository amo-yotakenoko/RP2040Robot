from machine import Pin, PWM, I2C
import sys
import select
import ssd1306

# OLEDディスプレイの初期化
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
display = ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)

# サーボの初期化 (16〜21番)
servos = [PWM(Pin(p)) for p in range(16, 22)]
for s in servos:
    s.freq(50)

def set_servo_angle(servo_obj, angle):
    mapped = int((angle - 0) * (180 - 10) / 180 + 10)
    servo_obj.duty_u16(int(1638 + (mapped / 180) * (7864 - 1638)))

# シリアル入力の監視準備
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

current_msg = "Waiting..."

while True:
    # シリアルからデータが来ていれば非ブロッキングで読み取る
    events = poll.poll(10)
    if events:
        line = sys.stdin.readline()
        if line:
            current_msg = line.strip()
            
            # 「0,90」のような形式であればサーボを動かす
            try:
                if ',' in current_msg:
                    parts = current_msg.split(',')
                    if len(parts) == 2:
                        i = int(parts[0])
                        angle = float(parts[1])
                        if 0 <= i < len(servos):
                            set_servo_angle(servos[i], angle)
            except:
                pass

    # LCD画面の更新
    # display.fill(0)
    # display.text("LCD Monitor:", 0, 0, 1)
    # display.text(current_msg, 0, 16, 1)
    # display.show()