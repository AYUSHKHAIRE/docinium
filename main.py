from docinium import DocShip

ship = DocShip()
ship.dock(33456)
ship.wait(5)

ship1 = DocShip()
try:
    ship1.dock(33456)
except Exception as e:
    print(f"Caught error: {e}")

ship1.wait(5)
ship.unDock()
