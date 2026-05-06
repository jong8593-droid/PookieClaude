import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import re
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')
PORT = 3000


def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

    def send_json(self, code, body):
        payload = json.dumps(body, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/registrations':
            records = read_data()
            self.send_json(200, {'total': len(records), 'data': records})
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/register':
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))

            name = (body.get('name') or '').strip()
            email = (body.get('email') or '').strip().lower()
            phone = (body.get('phone') or '').strip()

            if not name or not email or not phone:
                return self.send_json(400, {'error': 'กรุณากรอกข้อมูลให้ครบถ้วน'})

            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                return self.send_json(400, {'error': 'รูปแบบอีเมลไม่ถูกต้อง'})

            phone_digits = re.sub(r'[-\s]', '', phone)
            if not re.match(r'^\d{10}$', phone_digits):
                return self.send_json(400, {'error': 'เบอร์โทรต้องมี 10 หลัก'})

            records = read_data()
            if any(r['email'] == email for r in records):
                return self.send_json(409, {'error': 'อีเมลนี้ลงทะเบียนไปแล้ว'})

            record = {
                'id': int(datetime.now().timestamp() * 1000),
                'name': name,
                'email': email,
                'phone': phone,
                'registeredAt': datetime.now().isoformat()
            }
            records.append(record)
            write_data(records)
            self.send_json(201, {'message': 'ลงทะเบียนสำเร็จ', 'data': record})

    def do_DELETE(self):
        match = re.match(r'^/api/registrations/(\d+)$', self.path)
        if match:
            record_id = int(match.group(1))
            records = read_data()
            new_records = [r for r in records if r['id'] != record_id]
            if len(new_records) == len(records):
                return self.send_json(404, {'error': 'ไม่พบรายการ'})
            write_data(new_records)
            self.send_json(200, {'message': 'ลบเรียบร้อยแล้ว'})


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('', PORT), Handler)
    print(f"Server running at http://localhost:{PORT}")
    print(f"Registration form : http://localhost:{PORT}/form.html")
    print(f"Admin dashboard   : http://localhost:{PORT}/admin.html")
    print("กด Ctrl+C เพื่อหยุด server")
    server.serve_forever()
