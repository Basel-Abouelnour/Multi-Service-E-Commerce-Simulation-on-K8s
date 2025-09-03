from flask import Flask, jsonify
import os
import socket
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Constants
DEFAULT_PORT = 80
CONNECTION_TIMEOUT = 2

# Primary Target
TARGET_HOST = os.getenv("TARGET_HOST", "localhost")
TARGET_PORT = int(os.getenv("TARGET_PORT", DEFAULT_PORT))

# Secondary Target (optional)
TARGET_HOST2 = os.getenv("TARGET_HOST2")
TARGET_PORT2_RAW = os.getenv("TARGET_PORT2")
try:
    TARGET_PORT2 = int(TARGET_PORT2_RAW) if TARGET_PORT2_RAW else DEFAULT_PORT
except ValueError:
    TARGET_PORT2 = DEFAULT_PORT


def is_valid_port(port):
    return isinstance(port, int) and 0 < port < 65536


def check_host_connection(host, port):
    if not is_valid_port(port):
        return {
            "host": host,
            "port": port,
            "status": "failure",
            "message": f"Invalid port number: {port}"
        }

    try:
        logging.info(f"Checking connection to {host}:{port}")
        with socket.create_connection((host, port), timeout=CONNECTION_TIMEOUT):
            return {
                "host": host,
                "port": port,
                "status": "success",
                "message": f"Connected to {host}:{port}"
            }
    except Exception as e:
        return {
            "host": host,
            "port": port,
            "status": "failure",
            "message": f"Failed to connect to {host}:{port}",
            "error": str(e)
        }


@app.route('/')
def primary_connection():
    result = check_host_connection(TARGET_HOST, TARGET_PORT)
    return jsonify(result)


@app.route('/port2')
def secondary_connection():
    if not TARGET_HOST2:
        return jsonify({
            "status": "skipped",
            "message": "Second target not defined"
        })

    result = check_host_connection(TARGET_HOST2, TARGET_PORT2)
    return jsonify(result)


if __name__ == '__main__':
    logging.info("Starting Flask app on port 5000")
    app.run(host='0.0.0.0', port=5000)
