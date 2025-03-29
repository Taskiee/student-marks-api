from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import os

class handler(BaseHTTPRequestHandler):
    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        try:
            # Only handle /api route
            if not self.path.startswith('/api'):
                self.send_json_response(
                    {"error": "Not Found", "message": "Use /api endpoint"},
                    status_code=404
                )
                return

            # Parse query parameters
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            names = query.get('name', [])
            
            if not names:
                self.send_json_response(
                    {"error": "Bad Request", "message": "At least one name parameter is required"},
                    status_code=400
                )
                return

            # Load marks data
            data_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')
            with open(data_path) as f:
                data = json.load(f)
            
            # Get marks for requested names
            marks = [data.get(name, None) for name in names]
            
            # Prepare successful response
            self.send_json_response({"marks": marks})
            
        except FileNotFoundError:
            self.send_json_response(
                {"error": "Server Error", "message": "Marks data file not found"},
                status_code=500
            )
        except json.JSONDecodeError:
            self.send_json_response(
                {"error": "Server Error", "message": "Invalid marks data format"},
                status_code=500
            )
        except Exception as e:
            self.send_json_response(
                {"error": "Server Error", "message": str(e)},
                status_code=500
            )
