import socket
import threading
import base64
import random
import os
import sys


def handle_client(file_name, client_addr, server_addr):
    # 使用新端口传输数据
    port = random.randint(50000, 51000)
    new_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_sock.bind((server_addr, port))
    try:
        with open(f"files/{file_name}", "rb") as f:
            file_data = f.read()
        size = len(file_data)
        print(f"Sending {file_name} to {client_addr}, size {size} bytes")
        # 发送 OK 消息
        msg = f"OK {file_name} SIZE {size} PORT {port}"
        sock.sendto(msg.encode(), client_addr)
