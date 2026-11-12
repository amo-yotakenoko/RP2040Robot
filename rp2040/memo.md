python -m mpremote run servo_90.py






git clone https://github.com/micropython/micropython-lib.git
python -m mpremote cp lib/ssd1306.py :lib/ssd1306.py


python -m mpremote fs cp servo.py  :servo.py
python -m mpremote fs cp stewart_platform_serial.py  :main.py



python -m mpremote run stewart_platform_serial.py





python -m mpremote fs cp servo.py  :servo.py
python -m mpremote run armtest.py 