from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            names = query.get('name', [])
            
            if not names:
                return self.send_error(400, "Missing name parameter(s)")
            
            # Get absolute path to JSON file
            json_path = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')
            
            with open(json_path) as f:
                data = json.load(f)
            
            marks = [data.get(name) for name in names]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"marks": marks}).encode())
            
        except FileNotFoundError:
            self.send_error(404, "Data file not found")
        except json.JSONDecodeError:
            self.send_error(500, "Invalid data format")
        except Exception as e:
            self.send_error(500, str(e))
