import http.server
import logging
import socketserver

from app.private_config import working_path

PORT = 8000
logger: logging.Logger = logging.getLogger(name=__name__)
Handler = http.server.SimpleHTTPRequestHandler


# Create a server instance
with socketserver.TCPServer(
    server_address=("", PORT), RequestHandlerClass=Handler
) as httpd:
    logger.info(msg=f"Serving at port {PORT}")
    # Set the directory for the server
    httpd.directory = working_path  # type: ignore
    # Start the server
    httpd.serve_forever()
