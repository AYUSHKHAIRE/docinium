from utils.logger_config import logger
from utils.WebsocketClient import WebSocketClient
from utils.gui import ScreenController
from threading import Thread
import os
import time
from dotenv import load_dotenv

class DociniumExecutor:
    def __init__(self, uri, user_id, auth_token, ip, port):
        self.websocket_client = WebSocketClient(
            uri, 
            user_id, 
            auth_token, 
            ip, 
            port,
            message_handler=self.message_handler
        )
        self.screen_controller = ScreenController()

    def start(self):
        # Start the WebSocket client in a separate thread
        self.websocket_thread = Thread(target=self.websocket_client.run)
        self.websocket_thread.start()
        
        logger.info("Docinium Executor started and WebSocket client is running in a separate thread.")
        
    def message_handler(self, message):
        logger.debug(f"Received message through WebSocket handler: {message}")
        if message["type"] == "desktop_click":
            x_cord = message["message"]["click"]["x"]
            y_cord = message["message"]["click"]["y"]
            self.screen_controller.click_mouse(
                x = x_cord ,
                y = y_cord
            )

load_dotenv("/container/runtime.env")

url = os.getenv("DOCINIUM_EXECUTOR_URL")
user_id = os.getenv("DOCINIUM_EXECUTOR_USER_ID")
auth_token = os.getenv("DOCINIUM_EXECUTOR_AUTH_TOKEN")
ip = os.getenv("DOCINIUM_EXECUTOR_IP")
port = os.getenv("DOCINIUM_EXECUTOR_PORT")
 
logger.info(f"Docinium Executor configuration - URL: {url}, User ID: {user_id}, IP: {ip}, Port: {port}")
 
DE = DociniumExecutor(
    uri=url,
    user_id=user_id,
    auth_token=auth_token,
    ip=ip,
    port=port
)
DE.start()

time.sleep(10) 

logger.info("Docinium Executor is running. Press Ctrl+C to stop.")