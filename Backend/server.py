import socket


class CLI_conn:
    def __init__(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 65432))
        server.listen(1)
        print("Waiting for connection...")

        self.conn, addr = server.accept()
        print(f"Connected by {addr}")

    def recv(self):
        data = self.conn.recv(1024).decode()
        if not data:
            return
        return (f"C++ says: {data}")

    def snd(self, data):
        self.conn.sendall(f"Return from Python: {data}".encode())

    def kill(self):
        self.conn.close()

con = CLI_conn()

print(con.recv())
con.snd("Just checking...")

con.kill()
