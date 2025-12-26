import uuid
import sys
import os
from .logger_config import logger
from .WebsocketClient import WebSocketClient
import requests
import socket

def get_local_ip():
# Gets the primary network interface's IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # Google's public DNS
        local_ip = s.getsockname()[0]
    return local_ip

class Container:
    def __init__(self, port_to_connect, name=None):
        # Ensure project root is in sys.path
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        # Container name
        self.name = name or f"Cont_{str(uuid.uuid4())[:8]}"
        self.ws_client = None
        self.local_ip = get_local_ip()
        self.url_to_connect = f"{self.local_ip}:{port_to_connect}"
        self.port_to_connect = port_to_connect
        self._django_initialized = False

        # Connect to Django & WebSocket
        self._connect()

    def _preregister_user_http(self,base_url, username, password=None):
        """
        Calls Django preregister API and returns:
        (username, user_id, token)
        """
        url = f"http://{base_url}/connector/api/preregister/"
        payload = {
            "username": username,
            "password": password,
        }
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code != 201:
            raise RuntimeError(
                f"Preregister failed ({response.status_code}): {response.text}"
            )
        data = response.json()
        return username, data["user_id"], data["token"]

    def _connect(self):
        _ , user_id , token = self._preregister_user_http(
            username=f"docinium_container_{self.name}",
            base_url=self.url_to_connect
        )
        # Setup WebSocket
        websocket_uri = f"ws://{self.url_to_connect}/ws/docinium/{user_id}/"
        self.ws_client = WebSocketClient(
            uri=websocket_uri,
            user_id=user_id,
            auth_token=token,
            ip=self.local_ip,
            port=self.port_to_connect
        )

        # Start client
        self.ws_client.start_in_thread()
        logger.info(f"[docinium_engine > ws client] WebSocket client started for {self.name}")

        # Send a test message
        self.ws_client.send_message_thread_safe(type="hello", message="Hello, server!")
