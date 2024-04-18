from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from matrix_profile.analyzer import get_last_day_score
from utils import dt_to_str
import json
import datetime
import time
import threading


class MPServer(BaseHTTPRequestHandler):
    day = None
    score = None

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        response_data = {
            "day": dt_to_str(self.day),
            "score": round(self.score * 1000)
        }

        self.wfile.write(json.dumps(response_data).encode('utf-8'))


def update():
    print("\nStarting updating\n")
    print(datetime.datetime.now())

    day, score = get_last_day_score()
    MPServer.day = day
    MPServer.score = score

    print("\nInfo updated\n")
    print(datetime.datetime.now())


def update_forever():
    while True:
        update()
        time.sleep(3600)


def run(server_class=ThreadingHTTPServer, handler_class=MPServer, port=12345):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер будет запущен на порту {port}")
    update_thread = threading.Thread(target=update_forever)
    update_thread.daemon = True
    update_thread.start()
    print("Сервер запущен")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
