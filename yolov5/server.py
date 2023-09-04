# ソケットライブラリ取り込み
import socket
import pigpio
import time
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory

# サーバーIPとポート番号
IPADDR = "192.168.0.244"
PORT = 49152

SERVO_PIN_X = 18
SERVO_PIN_Y = 23

# pigpioを初期化
pi = pigpio.pi()

pi.set_servo_pulsewidth(SERVO_PIN_X, (90 / 180) * (2500 - 500) + 500)
pi.set_servo_pulsewidth(SERVO_PIN_Y, (90 / 180) * (2500 - 500) + 500)

PIN_LASER = 24
# LASERピン設定
factory = PiGPIOFactory()
led = LED(PIN_LASER, pin_factory=factory)

time.sleep(2)

# サーボモーターを特定の角度に設定する関数
x_angle_base = 90
y_angle_base = 90
def set_angle(angle,SERVO_PIN,xy,yon):
    global x_angle_base
    global y_angle_base

    if yon == 'on' :
        try:
            led.on()
        except:
            pass
        if str(xy) == 'x':
            angle = float(angle) - (float(angle) * 2)
            x_angle_base += float(angle)
            if float(x_angle_base) < 0 :
                x_angle_base = 0
            elif float(x_angle_base) > 180 :
                x_angle_base = 180
            else:
                pass
            print('x ',x_angle_base)
            assert 0 <= x_angle_base <= 180, '角度は0から180の間でなければなりません'
            # 角度を500から2500のパルス幅にマッピングする
            pulse_width = (x_angle_base / 180) * (2500 - 500) + 500
            # パルス幅を設定してサーボを回転させる
            pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

        else :
            y_angle_base += float(angle)
            if float(y_angle_base) < 0 :
                y_angle_base = 0
            elif float(y_angle_base) > 180 :
                y_angle_base = 180
            else:
                pass
            print('y ',y_angle_base)
            assert 0 <= y_angle_base <= 180, '角度は0から180の間でなければなりません'
            # 角度を500から2500のパルス幅にマッピングする
            pulse_width = (y_angle_base / 180) * (2500 - 500) + 500
            # パルス幅を設定してサーボを回転させる
            pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

    else :
        try:
            led.off()
        except:
            pass

# AF_INET：IPv4形式でソケット作成(省略可)
sock_sv = socket.socket(socket.AF_INET)
# IPアドレスとポート番号でバインド、タプルで指定
sock_sv.bind((IPADDR, PORT))
# サーバー有効化
sock_sv.listen()

# 接続・受信の無限ループ

while True:
    # クライアントの接続受付
    sock_cl, addr = sock_sv.accept()
    # ソケットから byte 形式でデータ受信
    data = sock_cl.recv(1024)
    #print(data.decode("utf-8"))
    angle_data = data.decode("utf-8")

    if angle_data == '' :
        set_angle(1,1,'y','off')
    else:
        print(angle_data)
        x_angle , y_angle , yon = angle_data.split(',')

        print('X' + str(float(x_angle)))
        set_angle(float(x_angle),SERVO_PIN_X,'x',str(yon))#yon yes or no
        print('Y' + str(float(y_angle)))
        set_angle(float(y_angle),SERVO_PIN_Y,'y',str(yon))


    # クライアントのソケットを閉じる
    sock_cl.close()
    #time.sleep(2.5)
