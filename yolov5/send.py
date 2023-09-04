import socket
import os
import sys
import time

args = sys.argv

abs_path = os.path.dirname(os.path.abspath(__file__))

temp_txt_path = str(abs_path) + '/temp.txt'

# サーバーIPとポート番号
IPADDR = "192.168.0.244"
PORT = 49152# ソケット作成
sock = socket.socket(socket.AF_INET)

while True:
    try :
        with open(str(temp_txt_path)) as f:
            point_data = f.read()
        # サーバーへ接続
        sock.connect((IPADDR, PORT))
        # byte 形式でデータ送信
        #point_data = str(export_num_x) + ',' + str(export_num_y) + ',' + str(objects_x)
        sock.send(point_data.encode("utf-8"))
        sys.exit()
    except :
        sys.exit()
