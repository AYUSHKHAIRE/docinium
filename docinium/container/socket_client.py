import time
import asyncio
import websockets
import json
from threading import Thread
from logger_config import logger
import socket

"""
WebSocket client to connect to the server and send/receive messages.
input:
    --uri: str : WebSocket server URI
    --user_id: str : Unique user ID
    --auth_token: str : Authentication token for the WebSocket server
algorithm:
    functions available:
        --start_in_thread : start operation in thread
        --run : run the event loop in a thread
        --connect : connect to the websocket server
        --send_message : send message to the websocket server
        --listen : listen for messages from the server
        --handle_message : handle incoming messages
        --close : close the websocket connection
        --send_message_thread_safe : send message from outside the websocket event loop
output:
    None
"""
class WebSocketClient:
    """
    WebSocket client to connect to the server and send/receive messages.
    input:
        --uri: str : WebSocket server URI
        --user_id: str : Unique user ID
        --auth_token: str : Authentication token for the WebSocket server
    algorithm:
        None
    output:
        None
    """
    def __init__(
        self, 
        port,
        user_id, 
        auth_token,
        ip
    ):
        if self.port is None:
            self.port = 33456  # Default port if not provided
        if self.ip is None:
            self.ip = self.get_local_ip()
        self.user_id = user_id
        self.auth_token = auth_token  
        self.websocket = None
        self.port = port
        self.ip = ip
        self.loop = asyncio.new_event_loop()
    
    def get_local_ip(self):
    # Gets the primary network interface's IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Google's public DNS
            local_ip = s.getsockname()[0]
        return local_ip
    """
    start operation in thread
    input:
        None
    algorithm:
        --create a thread
        --start the thread
    output:
        None
    """
    
    def start_in_thread(
        self
    ):
        thread = Thread(
            target=self.run, 
            daemon=True
        )
        thread.start()

    """ 
    run the event loop in a thread
    input:
        None
    algorithm:
        --set the event loop
        --run the event loop
    output:
        None
    """
    def run(
        self
    ):
        asyncio.set_event_loop(
            self.
            loop
        )
        self.loop.run_until_complete(
            self.connect()
        )

    """
    connect to the websocket server
    input:
        None
    algorithm:
        --create headers for the connection
        --connect to the websocket server
        --send registration message
        --listen for messages
    output:
        None
    """
    async def connect(
        self
    ):
        # Gets the primary network interface's IP address
        logger.warning(f"Local IP Address:{self.ip}")
        try:
            headers = {
                'Origin':f"http://{self.ip}:{self.port}",
                "Authorization": f"Bearer {self.auth_token}"
            }
            logger.debug(f"trying to connect to {self.ip}:{self.port} ...")
            self.websocket = await websockets.connect(
                f'{self.ip}:{self.port}', 
                additional_headers=headers
            )
            logger.info(f"[ CLIENT ] Connected to server at {self.ip}:{self.port} with authentication.")

            # Send registration message
            await self.send_message(
                type="register", 
                message="register request"
            )
            logger.info(f"[ CLIENT ] Sent registration message for user_id: {self.user_id}")
            # Start listening for server messages
            await self.listen()
        except Exception as e:
            logger.error(f"[ CLIENT ] Connection error: {e}")

    """
    send message to the websocket server
    input:
        --type: str : type of message
        --message: str : message to send
    algorithm:
        --send message
    output:
        None
    """
    async def send_message(
        self, 
        type, 
        message
    ):
        """Send a message over WebSocket."""
        if self.websocket:
            try:
                message_payload = {
                    "special": type,
                    "user_id": self.user_id,
                    "message": message,
                }
                await self.websocket.send(
                    json.dumps(
                        message_payload
                        )
                    )
                logger.info(f"[ CLIENT ] Sent message: {len(message_payload)}")
            except Exception as e:
                logger.error(f"[ CLIENT ] Error sending message: {e}")
        else:
            logger.warning("[ CLIENT ] WebSocket is not connected.")

    """
    listen for messages from the server
    input:
        None
    algorithm:
        --listen for messages
        --handle messages
    output:
        None
    """
    async def listen(
        self
    ):
        """Listen for messages from the server."""
        try:
            async for message in self.websocket:
                logger.info(f"[ CLIENT ] Received message: {len(message)}")
                await self.handle_message(
                    message
                )
        except Exception as e:
            logger.error(f"[ CLIENT ] Listening error: {e}")

    """
    handle incoming messages
    input:
        --message: str : incoming message
    algorithm:
        --handle message and set triggers
    output:
        None
    """
    async def handle_message(
        self, 
        message
    ):
        logger.warning(f'{message}')
        data = json.loads(message)
        if data.get("type") == "register":
            logger.info(f"[ CLIENT ] Registration successful for user_id: {self.user_id}")
            # Send hello message
            await self.send_message(
                type="hello", 
                message="Hello, server!"
            )
        elif data.get("type") == "hello":
            logger.info(f"[ CLIENT ] Server says: {data['message']}")

    """
    close the websocket connection
    input:
        None
    algorithm:
        --close the websocket connection
    output:
        None
    """
    async def close(
        self
    ):
        if self.websocket:
            await self.websocket.close()
            logger.info("[ CLIENT ] WebSocket connection closed.")

    """
    send message from outside the websocket event loop
    input:
        --type: str : type of message
        --message: str : message to send
    algorithm:
        --send message
    output:
        None
    """
    def send_message_thread_safe(
        self, 
        type, 
        message
    ):
        if self.loop.is_running():
            asyncio.run_coroutine_threadsafe(
                self.send_message(
                    type=type, 
                    message=message
                ), 
                self.loop
            )
        else:
            logger.warning("[ CLIENT ] WebSocket event loop is not running.")
