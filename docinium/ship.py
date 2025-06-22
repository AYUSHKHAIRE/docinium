# built in packages
import socket
import errno
import subprocess
import os
import time

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
    
    def __init__(self):
        """
        Initializes the DocShip instance with default values.
        """
        self.port = None
        self.engine_process = None

    def _is_port_in_use(self, port):
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
                    ("127.0.0.1", port)
                )
                return False  # Port is free
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    return True  # Port is already in use
                else:
                    raise

    def _start_the_engine(self, port):
        """
        Starts the Django engine on the specified port.

        Args:
            port (int): The port number to run the server on.

        Raises:
            DockShipError: If the subprocess fails to start.
        """
        manage_py_path = os.path.abspath("docinium/docinium_engine/manage.py")
        try:
            self.engine_process = subprocess.Popen(
                ["python", manage_py_path, "runserver", str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except Exception as e:
            raise DockShipError() from e

    def dock(self, port=12345):
        """
        Attempts to start the Django engine on the specified port.

        Args:
            port (int, optional): The port number to use. Defaults to 12345.

        Raises:
            PortInUseError: If the specified port is already occupied.
            DockShipError: If the engine fails to start.
        """
        self.port = port
        if self._is_port_in_use(port):
            raise PortInUseError(port)
        try:
            self._start_the_engine(port)
            print(f"Docked the ship at http://localhost:{self.port}...")
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
            if self._is_port_in_use(self.port):
                raise UnDockShipError()
            print(f"Ship on port {self.port} has been undocked successfully.")
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
        # Placeholder for actual loading logic
        # This could involve pulling a Docker image, etc.
        time.sleep(2)