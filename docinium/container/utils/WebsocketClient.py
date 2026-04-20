# Standard Library
import json
import asyncio
from threading import Thread, RLock
from multiprocessing import shared_memory
from multiprocessing.shared_memory import SharedMemory
import websockets
from utils.logger_config import logger

"""
WebSocket docinium_container > websocket client to connect to the server and send/receive messages.
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
    WebSocket docinium_container > websocket client to connect to the server and send/receive messages.
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
        uri, 
        user_id, 
        auth_token,
        ip,
        port
    ):
        self.uri = uri
        self.user_id = user_id
        self.auth_token = auth_token  
        self.websocket = None
        self.ip = ip
        self.port = port
        self.loop = asyncio.new_event_loop()
    
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
        # logger.warning(f"Local IP Address:{self.ip}")
        try:
            headers = {
                'Origin':f"http://{self.ip}:{self.port}",
                "Authorization": f"Bearer {self.auth_token}"
            }
            logger.info(f"[ docinium_container > websocket client ] trying to connect to {self.uri}")
            self.websocket = await websockets.connect(
                self.uri, 
                additional_headers=headers
            )
            logger.info(f"[ docinium_container > websocket client ] Connected to server at {self.uri} with authentication.")

            # Send registration message
            await self.send_message(
                type="register", 
                message="register request"
            )
            logger.info(f"[ docinium_container > websocket client ] Sent registration message for user_id: {self.user_id}")
            # Start listening for server messages
            await self.listen()
        except Exception as e:
            logger.error(f"[ docinium_container > websocket client ] Connection error: {e}")

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
                logger.info(f"[ docinium_container > websocket client ] Sent message: {len(message_payload)}")
            except Exception as e:
                logger.error(f"[ docinium_container > websocket client ] Error sending message: {e}")
        else:
            logger.warning("[ docinium_container > websocket client ] WebSocket is not connected.")

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
                logger.info(f"[ docinium_container > websocket docinium_container > websocket client ] Received message: {len(message)}")
                await self.handle_message(
                    message
                )
        except Exception as e:
            logger.error(f"[ docinium_container > websocket client ] Listening error: {e}")

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
            logger.info("[ docinium_container > websocket client ] WebSocket connection closed.")

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
            logger.warning("[ docinium_container > websocket client ] WebSocket event loop is not running.")

    async def handle_message(
        self, 
        message
    ):
        logger.info(f'[docinium_container > websocket docinium_container > websocket client]{message}')
        data = json.loads(message)
        if data.get("type") == "register":
            logger.info(f"[ docinium_container > websocket docinium_container > websocket client ] Registration successful for user_id: {self.user_id}")
            # Send hello message
            await self.send_message(
                type="hello", 
                message="Hello, server!"
            )