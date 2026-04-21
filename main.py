from docinium import DocShip
from docinium import Container

PORT = 23501

ship = DocShip(name="ship 1", port=PORT)
ship.dock()

container = Container(
    name = "container_1",
    port_to_connect = PORT
)

ship.mount(container)

ship.wait(5)

container.send_message(
    type="desktop_click", 
    message={
        "click":{
            "x": 100,
            "y": 200
        }
    }
)

ship.unDock()