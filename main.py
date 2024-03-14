import json
import mimetypes
import os
import pathlib
import socket
import threading
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        base_directory = 'front-init/front-init'
        if pr_url.path == '/':
            self.send_html_file(os.path.join(base_directory, 'index.html'))
        elif pr_url.path == '/message':
            self.send_html_file(os.path.join(base_directory, 'message.html'))
        else:
            file_path = os.path.join(base_directory, pr_url.path[1:])  # Створюємо повний шлях
            if pathlib.Path(file_path).exists():
                self.send_static(file_path)  # Тепер передаємо повний шлях
            else:
                self.send_html_file(os.path.join(base_directory, 'error.html'), 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, filepath):
        self.send_response(200)
        mt = mimetypes.guess_type(filepath)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(filepath, 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        print(data_dict)
        udp_host = 'localhost'
        udp_port = 5000
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (udp_host, udp_port))
        sock.close()

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


def store_data(data):
    storage_dir = 'front-init/front-init/storage'
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
    with open(os.path.join(storage_dir, 'data.json'), 'w') as f:
        json.dump(data, f)


def start_udp_server(host='localhost', port=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f'UDP Server listening on {host}:{port}')

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(f'Received message: {data} from {addr}')

        # Convert byte string to dictionary
        data_str = data.decode()
        data_dict = {k: v for k, v in [kv.split('=') for kv in data_str.split('&')]}
        print(f'Data received: {data_dict}')

        # Store data in json file
        store_data(data_dict)


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 8000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def main():
    http_server_thread = threading.Thread(target=run)
    http_server_thread.start()
    start_udp_server()


if __name__ == '__main__':
    main()
