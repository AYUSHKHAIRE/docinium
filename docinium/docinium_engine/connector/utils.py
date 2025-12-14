import socket

def get_local_ip():
# Gets the primary network interface's IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # Google's public DNS
        local_ip = s.getsockname()[0]
    return local_ip