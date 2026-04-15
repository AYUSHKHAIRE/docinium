from docinium import DocShip
from docinium import Container

PORT = 23486

ship = DocShip(name="ship 1", port=PORT)
ship.dock()

container = Container(
    name = "container_1",
    port_to_connect = PORT
)

ship.mount(container)

ship.wait(500)

ship.unDock()