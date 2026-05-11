from docinium import DocShip
from docinium import Container

PORT = 23507

ship = DocShip(name="ship 1", port=PORT)
ship.dock()

container = Container(
    name = "container_1",
    port_to_connect = PORT
)

ship.mount(container)

ship.wait(60)

container.send_message(
    type="desktop_click", 
    message={
        "click":{
            "x": 30,
            "y": 30
        }
    }
)

ship.wait(300)

ship.unDock()