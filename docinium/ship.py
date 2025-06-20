class DocShip:
    def __init__(self):
        self.port = None
        
    def dock(self,port = 12345):
        self.port = port
        print(f"Docked the ship at port {self.port}...")