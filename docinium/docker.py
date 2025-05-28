from .logger_config import logger
from .socket_server import SocketServer

class DockerManager:
    def __init__(self , host = 'localhost' , port = 5454):
        self.containers = []
        self.port = port
        self.host = host
        self.socket_server = None
        self.server = SocketServer(
            host = host ,
            port = port
        )
        self.server.start()