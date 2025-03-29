from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            names = query.get('name', [])
            
            data_path = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')
            with open(data_path) as f:
                data = json.load(f)
            
            response = {"marks": [data.get(name, None) for name in names]}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {"error": "Internal Server Error", "message": str(e)}
            self.wfile.write(json.dumps(error_response).encode())
