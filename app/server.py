import http.server
import logging
import socketserver
from pathlib import Path

PORT = 8000
logger = logging.getLogger(__name__)
Handler = http.server.SimpleHTTPRequestHandler

# Change the current directory to the directory containing your files
directory = Path(__file__).parent.parent / "files/"

# Create a server instance
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    logger.info("Serving at port", PORT)
    # Set the directory for the server
    httpd.directory = directory  # type: ignore
    # Start the server
    httpd.serve_forever()
