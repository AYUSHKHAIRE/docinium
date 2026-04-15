from docinium import DocShip
from docinium import Container

PORT = 23494

ship = DocShip(name="ship 1", port=PORT)
ship.dock()

container = Container(
    name = "container_1",
    port_to_connect = PORT
)

container_2 = Container(
    name = "container_2",
    port_to_connect = PORT
)

container_3 = Container(
    name = "container_3",
    port_to_connect = PORT
)

ship.mount(container)
ship.mount(container_2)
ship.mount(container_3)

ship.wait(500)

ship.unDock()