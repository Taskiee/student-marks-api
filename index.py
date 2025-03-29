from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Parse query parameters
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            names = query.get('name', [])
            
            # Load marks data from the same directory
            data_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')
            with open(data_path) as f:
                data = json.load(f)
            
            # Get marks for requested names
            marks = [data.get(name, None) for name in names]
            
            # Prepare response
            response = {"marks": marks}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Error processing request: {str(e)}")
