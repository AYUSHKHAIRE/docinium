from docinium import DocShip

ship = DocShip(name="ship 1", port=23456)
ship.dock()
ship.wait(500)

ship.unDock()
