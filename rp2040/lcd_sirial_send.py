import serial
import time

PORT = "COM10"
BAUD_RATE = 115200

try:
    # シリアルポートを開く
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(1) # 接続安定待ち
    
    print(f"--- {PORT} に接続しました ---")
    print("文字を入力してEnterを押すと、PicoのLCDに表示されます。")
    print("（例: 0,90 と打つとサーボが動き、文字と打つとLCDに文字が出ます）\n")

    while True:
        # PC側でキーボード入力を待機
        msg = input("送信する文字 > ")
        
        # 改行付きで送信
        ser.write((msg + "\n").encode("utf-8"))
        print(f"-> 送信完了: {msg}")

except KeyboardInterrupt:
    print("\n終了します。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("ポートを閉じました。")