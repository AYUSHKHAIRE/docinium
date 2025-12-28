from docinium import DocShip
from docinium import Container

PORT = 23488

ship = DocShip(name="ship 1", port=PORT)
ship.dock()

container = Container(
    name = "container 1",
    port_to_connect = PORT
)



ship.wait(500)

ship.unDock()