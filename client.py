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

