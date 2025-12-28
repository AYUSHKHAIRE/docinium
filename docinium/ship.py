# built in packages
import socket
import errno
import subprocess
import os
import time
from dotenv import load_dotenv
from docinium.container.logger_config import logger
from docinium.dockerclient import DockerManager
from docinium.glucamole_manager import GuacamoleClient
import threading
import uuid

# my own functionalities
from docinium.exceptions import (
    PortInUseError, 
    DockShipError, 
    UnDockShipError
)

"""
Attempts to start the Django engine on the specified port.

Raises:
    DockShipError: this error is raised when it fails to start the Django server on the port.
    PortInUseError: this error is raised when the port is already in use.
    UnDockShipError: this error is raised when the port is still in use after termination of the Django server.
"""

class DocShip:
    """
    A class to manage docking and undocking of the backend Django engine.

    Attributes:
        port (int): The port on which the server is running.
        engine_process (Popen): Reference to the subprocess running the server.
    """
    
    def __init__(self,name, port):
        """
        Initializes the DocShip instance with default values.
        """
        if name:
            self.name = name
        else:
            id = str(uuid.uuid4())[:8]
            self.name = "DocShip_" + id
        self.port = port
        self.engine_process = None
        self.docker_manager = DockerManager()
        self.guacomole_manager = None
        self.docker_engine_thread = None

    def _is_port_in_use(self):
        """
        Checks if a given port is currently in use.

        Args:
            port (int): The port number to check.

        Returns:
            bool: True if the port is in use, False otherwise.

        Raises:
            socket.error: If there is an error checking the port.
        """
        with socket.socket(
            socket.AF_INET, 
            socket.SOCK_STREAM
        ) as s:
            try:
                s.bind(
                    ("0.0.0.0", self.port)
                )
                return False  # Port is free
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    return True  # Port is already in use
                else:
                    raise

    def stream_logs(self,proc):
        for line in proc.stdout:
            logger.info(f"[docinium_engine > django] {line.strip()}")
            
    def _start_the_engine(self):
        """
        Starts the Django engine on the specified port.

        Args:
            port (int): The port number to run the server on.

        Raises:
            DockShipError: If the subprocess fails to start.
        """
        manage_py_path = os.path.abspath("docinium/docinium_engine/manage.py")
        try:
            import sys
            self.engine_process = subprocess.Popen(
                [sys.executable, "-u" ,manage_py_path, "runserver", f"0.0.0.0:{self.port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1 
            )
            time.sleep(3)
            threading.Thread(target=self.stream_logs, args=(self.engine_process,), daemon=True).start()
            # logger.info("Starter command for django ran .")
        except Exception as e:
            raise DockShipError() from e

    def _check_image(self, image_name):
        """
        Checks if the specified Docker image exists.

        Args:
            image_name (str): The name of the Docker image to check.

        Returns:
            bool: True if the image exists, False otherwise.
        """
        return self.docker_manager.check_if_image_exists(image_name)

    def _check_and_pull_required_images(self, image_names):
        """
        Checks if the specified Docker image exists, and pulls it if it doesn't.

        Args:
            image_names (list): The list of Docker image names to check and pull.
        """
        for image_name in image_names:
            if not self._check_image(image_name):
                logger.warning(f"Docker image {image_name} does not exist. Attempting to pull it...")
                logger.info(f"Pulling Docker image: {image_name}")
                status = self.docker_manager.pull_image(image_name)
                if status:
                    logger.info(f"Docker image {image_name} pulled successfully.")
            else:
                logger.info(f"Docker image {image_name} already exists.")
        return True

    def _setup(self):
        os.environ["PORT_TO_USE_FOR_DOCINIUM"] = str(self.port)
        # pull the required images for docker
        required_images  = {
            "redis:latest": {
                "container_name": "docinium_redis",
                "port_map": {"6379/tcp": 6379},
                "network_name": "docinium_network"
            },
            "jwetzell/guacamole:latest": {
                "container_name": "docinium_guacamole",
                "port_map": {"8080/tcp": 8080},
                "network_name": "docinium_network",
                "volumes": {
                    "guac_config": "/config"
                }
            }
        }
        if self._check_and_pull_required_images(required_images.keys()):
            logger.info("All required Docker images are present.")
        # create or check new docker network
        network_name = "docinium_network"
        self.docker_manager.create_docker_network(network_name)
        for cont_k , cont_v in required_images.items():
            if self.docker_manager.check_if_docker_container_exist(cont_v["container_name"]):
                self.docker_manager.delete_docker_container(cont_v["container_name"])
            self.docker_manager.spin_up_docker_container(
                image_name=cont_k,
                container_name=cont_v["container_name"],
                network_name=cont_v["network_name"],
                port_map=cont_v["port_map"],
                detach=True
            )
        # start the engine
        self._start_the_engine()
        # attempt guacamole
        self.guacomole_manager = GuacamoleClient()
        users = self.guacomole_manager.list_all_users()
        # logger.debug(f"Guacamole users {users}")
        logger.info(f"Docked the {self.name} at http://0.0.0.0:{self.port} successfully...")

    def dock(self):
        """
        Attempts to start the Django engine on the specified port.

        Args:
            port (int, optional): The port number to use. Defaults to 12345.

        Raises:
            PortInUseError: If the specified port is already occupied.
            DockShipError: If the engine fails to start.
        """
        if self._is_port_in_use():
            raise PortInUseError(self.port)
        try:
            self._setup()
            image_exist = self._check_image("docinium_container")
            if not image_exist:
                logger.warning("Docker image 'docinium_container' does not exist.")
            else:
                logger.info("Docker image 'docinium_container' found.")
        except DockShipError as e:
            raise e
    
    def wait(self, time_in_seconds=10):
        """
        Pauses the current process to allow the engine to initialize or stay up.

        Args:
            time_in_seconds (int, optional): Duration to wait. Defaults to 10 seconds.
        """
        time.sleep(time_in_seconds)

    def unDock(self):
        """
        Stops the running engine process and frees the port.

        Raises:
            UnDockShipError: If the port is still in use after termination.
        """
        if self.engine_process:
            self.engine_process.terminate()
            self.engine_process.wait()
            if self._is_port_in_use():
                raise UnDockShipError()
            print(f"Ship on port {self.port} has been undocked successfully.")
            required_images  = {
                    "redis:latest": {
                        "container_name": "docinium_redis",
                        "port_map": {"6379/tcp": 6379},
                        "network_name": "docinium_network"
                    },
                    "oznu/guacamole:latest": {
                        "container_name": "docinium_guacamole",
                        "port_map": {"8080/tcp": 8080},
                        "network_name": "docinium_network",
                        "volumes": {
                            "guac_config": "/config"
                        }
                    }
                }
            for cont_k , cont_v in required_images.items():
                self.docker_manager.delete_docker_container(cont_v["container_name"])
        else:
            print("No engine process to stop.")
        self.port = None
        
    def load_the_container(self , container_name):
        """
        Loads the specified docker container.

        Args:
            container_name (str): The name of the container to load.
        """
        print(f"Loading the container: {container_name}...")