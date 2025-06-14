import socket
import sys
import base64
import time

def send_and_receive(sock, msg, server, retries=5):
    timeout = 1
    for i in range(retries):
        sock.sendto(msg.encode(), server)
        sock.settimeout(timeout)
        try:
            data, addr = sock.recvfrom(2048)
            return data.decode(), addr
        except socket.timeout:
            timeout *= 2
    return None, None

def download_file(server_host, port, file_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = (server_host, port)

    msg = f"DOWNLOAD {file_name}"
    response, _ = send_and_receive(sock, msg, server)
    if not response:
        print(f"Download request for {file_name} failed.")
        return

    if response.startswith("ERR"):
        print(f"Server does not have file {file_name}")
        return

    parts = response.split()
    size = int(parts[4])
    data_port = int(parts[6])
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  