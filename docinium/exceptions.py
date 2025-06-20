class PortInUseError(Exception):
    def __init__(self, port):
        super().__init__(f"Port {port} is already in use. Please choose a different port.")
        self.port = port

class DockShipError(Exception):
    def __init__(self):
        super().__init__("Failed to dock the ship: Could not start the engine.")

class UnDockShipError(Exception):
    def __init__(self):
        super().__init__("Failed to undock the ship: Port is still in use after termination.")
