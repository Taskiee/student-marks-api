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
                self.send_error_response(400, "At least one name parameter is required")
                return
            
            # Get the absolute path to the JSON file
            json_path = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')
            
            # Read and parse the JSON file
            with open(json_path) as f:
                student_data = json.load(f)
            
            # Get marks for requested names
            marks = [student_data.get(name, None) for name in names]
            
            # Send successful response
            self.send_json_response(200, {"marks": marks})
            
        except FileNotFoundError:
            self.send_error_response(404, "Marks data file not found")
        except json.JSONDecodeError:
            self.send_error_response(500, "Invalid JSON data format")
        except Exception as e:
            self.send_error_response(500, f"Internal server error: {str(e)}")

    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def send_error_response(self, status_code, message):
        self.send_json_response(status_code, {
            "error": self.responses[status_code][0],
            "message": message,
            "status": status_code
        })
