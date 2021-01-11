import socket
def check(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return False# s.connect_ex(('localhost', int(port))) == 0
