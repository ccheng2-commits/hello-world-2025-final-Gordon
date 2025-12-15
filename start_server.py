#!/usr/bin/env python3
"""
IRIS#1 - Digital Biometrics
Simple HTTP server to serve frontend and data files.
This allows the frontend to load codes_index.json via HTTP.
"""

import http.server
import socketserver
import os
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve files from multiple directories"""
    
    def end_headers(self):
        # Add CORS headers to allow loading from different origins
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        # Parse the path
        path = self.path.split('?')[0]  # Remove query string
        
        # Route /data/ requests to data directory
        if path.startswith('/data/'):
            file_path = DATA_DIR / path[6:]  # Remove '/data/' prefix
            if file_path.exists() and file_path.is_file():
                self.serve_file(file_path)
                return
        
        # Route root and /frontend/ to frontend directory
        if path == '/' or path == '/index.html':
            file_path = FRONTEND_DIR / "index.html"
            if file_path.exists():
                self.serve_file(file_path)
                return
        
        # Try to serve from frontend directory
        if path.startswith('/'):
            file_path = FRONTEND_DIR / path[1:]
            if file_path.exists() and file_path.is_file():
                self.serve_file(file_path)
                return
        
        # Default: serve from current directory
        super().do_GET()
    
    def serve_file(self, file_path):
        """Serve a file with appropriate content type"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Determine content type
            content_type = 'application/octet-stream'
            if file_path.suffix == '.html':
                content_type = 'text/html'
            elif file_path.suffix == '.js':
                content_type = 'application/javascript'
            elif file_path.suffix == '.json':
                content_type = 'application/json'
            elif file_path.suffix == '.css':
                content_type = 'text/css'
            elif file_path.suffix == '.jpg' or file_path.suffix == '.jpeg':
                content_type = 'image/jpeg'
            elif file_path.suffix == '.png':
                content_type = 'image/png'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error serving file: {e}")

def start_server():
    """Start the HTTP server"""
    os.chdir(PROJECT_ROOT)
    
    handler = CustomHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("=" * 60)
        print("IRIS#1 - Digital Biometrics Server")
        print("=" * 60)
        print(f"\n🌐 Server running at: http://localhost:{PORT}")
        print(f"📁 Frontend: http://localhost:{PORT}/index.html")
        print(f"📊 Data API: http://localhost:{PORT}/data/codes_index.json")
        print("\nPress Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")

if __name__ == "__main__":
    start_server()

