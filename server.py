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

        # 启动数据块响应循环
        while True:
            req, addr = new_sock.recvfrom(2048)
            msg = req.decode()
            if msg.startswith(f"FILE {file_name} GET"):
                parts = msg.split()
                start = int(parts[5])
                end = int(parts[7])
                chunk = file_data[start:end + 1]
                encoded = base64.b64encode(chunk).decode()
                response = f"FILE {file_name} OK START {start} END {end} DATA {encoded}"
                new_sock.sendto(response.encode(), addr)
            elif msg.startswith(f"FILE {file_name} CLOSE"):
                new_sock.sendto(f"FILE {file_name} CLOSE_OK".encode(), addr)
                break
    except FileNotFoundError:
        err = f"ERR {file_name} NOT_FOUND"
        sock.sendto(err.encode(), client_addr)
    finally:
        new_sock.close()

# 主入口
if __name__ == "__main__":
    port = int(sys.argv[1])
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("", port))
    print(f"Server running on UDP port {port}")

    while True:
        msg, addr = server.recvfrom(1024)
        if msg.startswith(b"DOWNLOAD"):
            file_name = msg.decode().split()[1]
            threading.Thread(target=handle_client, args=(file_name, addr, '')).start()