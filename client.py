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

    received = bytearray()
    for start in range(0, size, 1000):
        end = min(start + 999, size - 1)
        msg = f"FILE {file_name} GET START {start} END {end}"
        chunk, _ = send_and_receive(data_sock, msg, (server_host, data_port))
        if chunk and "DATA" in chunk:
            encoded_data = chunk.split("DATA ")[1]
            decoded = base64.b64decode(encoded_data)
            received.extend(decoded)
            print(f"Received {start}-{end}")
# 发送关闭
    send_and_receive(data_sock, f"FILE {file_name} CLOSE", (server_host, data_port))
    with open(file_name, "wb") as f:
        f.write(received)
    print(f"File {file_name} downloaded.")

# 主入口
if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    list_file = sys.argv[3]

    