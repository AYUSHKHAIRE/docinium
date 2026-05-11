# Docinium

Your container desktops, one browser away.

---

## Introduction

Docinium is a platform for orchestrating and interacting with multiple containerized desktop environments through a unified browser interface.

- Built using Python and Docker, Docinium enables secure, isolated, and scalable desktop sessions that can be accessed and controlled directly from the web. It is designed to simplify remote desktop infrastructure, browser-based interaction, and multi-container desktop management for developers, automation systems, and accessibility-focused applications.
---

## Setup

### Clone the repository

```sh
git clone https://github.com/AYUSHKHAIRE/docinium
cd docinium
```

### Create a Python environment

```sh
python3.12 -m venv env
```

### Activate the environment

```sh
source env/bin/activate
```

### Install dependencies

```sh
pip install -r requirements.txt
```

### Build the Docker image

```sh
cd docinium/container/
docker build -t docinium_container .
cd ../..
```

---

## Get Started

You can write your own orchestration logic or refer to `main.py`.

```python
"""
Core imports.
"""

from docinium import DocShip
from docinium import Container


"""
Think of Docinium like a ship management system.

- A DocShip manages multiple containers.
- Each Container runs an isolated desktop environment.
- The ship docks on a port and allows browser interaction.
"""


"""
Port where the ship will dock.
"""
PORT = 23505


"""
Create and dock the ship.
"""
ship = DocShip(
    name="ship_1",
    port=PORT
)

ship.dock()


"""
Create a desktop container.
"""
container = Container(
    name="container_1",
    port_to_connect=PORT
)


"""
Mount the container onto the ship.
"""
ship.mount(container)


"""
Keep the ship running.
"""
ship.wait(60)


"""
Interact with the desktop remotely.
"""
container.send_message(
    type="desktop_click",
    message={
        "click": {
            "x": 30,
            "y": 30
        }
    }
)


"""
Wait before shutting down.
"""
ship.wait(300)


"""
Undock and clean up resources.
"""
ship.unDock()
```

---

## Demo

According to the example above, you can access the web interface at:

```text
http://0.0.0.0:23505
```

You should see a screen like this:

![Home Page](https://github.com/AYUSHKHAIRE/docinium/blob/main/public/images/1.png?raw=true)

You can now navigate to the login page and log in using the following credentials:

```text
Username: admin
Password: admin
```

![Login Page](https://github.com/AYUSHKHAIRE/docinium/blob/main/public/images/2.png?raw=true)

After logging in, return to the home page.

![Dashboard](https://github.com/AYUSHKHAIRE/docinium/blob/main/public/images/3.png?raw=true)

On the sidebar, you will see the **Admin** and **Containers** sections.

![Sidebar](https://github.com/AYUSHKHAIRE/docinium/blob/main/public/images/4.png?raw=true)

Inside the Containers page, you can view all currently docked containers on the ship, along with:
- Direct desktop access links
- A direct link to the Apache Guacamole dashboard

You can open the Guacamole page and log in using:

```text
Username: guacadmin
Password: guacadmin
```

![Guacamole Login](https://github.com/AYUSHKHAIRE/docinium/blob/main/public/images/5.png?raw=true)

Returning to the Containers page, you can click the direct desktop button for any running container.

This will open the containerized desktop environment in your browser.

![Desktop Container](https://github.com/AYUSHKHAIRE/docinium/blob/main/public/images/6.png?raw=true)

Additionally, Docinium provides a Django admin panel where you can manage users and monitor active RDP connections.

![Django Admin](https://github.com/AYUSHKHAIRE/docinium/blob/main/public/images/7.png?raw=true)

---

---

# Architecture

![Docinium Architecture](https://github.com/AYUSHKHAIRE/docinium/blob/main/public/images/docinium_architecture.png?raw=true)

Docinium is built as a distributed desktop orchestration platform that combines Docker containers, Django, WebSockets, Apache Guacamole, and a high-level Python SDK into a unified system for managing browser-accessible desktop environments.

The architecture is designed to provide:

- Secure isolated desktop environments
- Real-time browser interaction
- Multi-container orchestration
- Remote desktop accessibility
- Scalable communication through WebSockets
- Developer-friendly automation APIs

---

## Core Components

### 1. Docinium SDK (Python Library)

The Docinium SDK is the main orchestration layer used by developers.

It is responsible for:

- Spinning up Docker desktop containers
- Managing container lifecycle
- Mounting containers onto ships
- Connecting containers to the central server
- Handling orchestration logic
- Managing WebSocket communication

The SDK exposes high-level abstractions such as:

```python
ship = DocShip(...)
container = Container(...)
```

This allows developers to manage multiple desktop environments programmatically using Python.

---

### 2. Django Engine

The Django engine acts as the central control server of Docinium.

Responsibilities include:

- User authentication
- Session management
- Web interface rendering
- Managing desktop metadata
- Recording RDP connections
- Creating Guacamole connection mappings
- Managing active WebSocket connections
- Providing the unified browser interface

The Django backend is powered using:

- Django
- Django Channels
- ASGI
- WebSockets

---

### 3. Redis Communication Layer

Redis is used as the real-time communication backbone for Django Channels.

It handles:

- WebSocket channel layers
- Real-time event distribution
- Connection synchronization
- Async communication support

Redis enables scalable bidirectional communication between:

- Django
- Browser clients
- Desktop containers

---

### 4. Apache Guacamole

Apache Guacamole provides browser-based remote desktop streaming.

Docinium uses Guacamole to expose desktop environments directly inside the browser without requiring local RDP clients.

Guacamole is responsible for:

- Browser-accessible desktop sessions
- RDP proxying
- Remote desktop streaming
- User desktop access

The Django engine dynamically manages Guacamole users and RDP connection records.

---

### 5. Desktop Containers

Each desktop environment runs inside an isolated Docker container.

Every container includes:

- XFCE desktop environment
- XRDP server
- PulseAudio support
- Google Chrome
- Python runtime
- Internal communication scripts
- WebSocket client connection to the server

Each container operates independently with Docker-level isolation including:

- Filesystem isolation
- Network isolation
- Process isolation

This enables secure multi-desktop orchestration.

---

## Communication Flow

### Container Lifecycle

```text
Python SDK
    ↓
Docker Container Creation
    ↓
Desktop Container Starts
    ↓
Container Connects via WebSocket
    ↓
Django Registers Connection
    ↓
Guacamole RDP Mapping Created
    ↓
Desktop Becomes Available in Browser
```

---

## Browser Interaction Flow

```text
User Browser
    ↓
Django Web Interface
    ↓
Apache Guacamole
    ↓
XRDP inside Container
    ↓
XFCE Desktop Environment
```

---

## Real-Time Communication Flow

```text
Desktop Container
    ↕ WebSocket
Django Channels
    ↕ Redis
Browser Interface
```

This allows real-time communication between:

- Desktop containers
- Backend services
- Browser clients

---

## Internal Project Structure

### SDK Layer

```text
.
├── commands.txt
├── docinium
│   ├── container
│   │   ├── commands.txt
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── script.py
│   │   └── utils
│   │       ├── gui.py
│   │       ├── logger_config.py
│   │       └── WebsocketClient.py
│   ├── container_manager.py
│   ├── docinium_engine
│   │   ├── connector
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── consumers.py
│   │   │   ├── __init__.py
│   │   │   ├── logger_config.py
│   │   │   ├── models.py
│   │   │   ├── routing.py
│   │   │   ├── services.py
│   │   │   ├── tests.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── core
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── tests.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── db.sqlite3
│   │   ├── docinium_engine
│   │   │   ├── asgi.py
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
│   │   ├── manage.py
│   │   ├── static
│   │   │   ├── css
│   │   │   │   ├── home.css
│   │   │   │   └── style.css
│   │   │   └── js
│   │   │       └── script.js
│   │   ├── support
│   │   │   └── utils.py
│   │   └── templates
│   │       ├── accounts
│   │       │   └── login.html
│   │       ├── base.html
│   │       └── core
│   │           ├── containers.html
│   │           └── index.html
│   ├── docinium_engine_api.py
│   ├── dockerclient.py
│   ├── exceptions.py
│   ├── glucamole_manager.py
│   ├── __init__.py
│   ├── logger_config.py
│   ├── ship.py
│   └── WebsocketClient.py
├── docinium_container.log
├── docinium.log
├── main.py
├── public
├── README.md
├── requirements.txt
├── scripts
│   └── stop_docinium_containers.sh
└── structure.md

17 directories, 59 files
```

Handles orchestration, Docker management, WebSocket communication, and Guacamole integration.

---

### Django Engine

```text
docinium/docinium_engine/
```

Contains:

- Authentication system
- Web UI
- Django Channels consumers
- Models
- Routing
- APIs
- WebSocket services

---

### Desktop Container Runtime

```text
docinium/container/
```

Contains:

- Dockerfile
- Desktop startup scripts
- GUI interaction logic
- Container-side WebSocket client
- Audio and desktop environment setup

---

## Security and Isolation

Docinium relies on Docker containerization to provide isolation between desktop sessions.

Each desktop container has:

- Independent processes
- Isolated networking
- Separate filesystem space
- Dedicated desktop session

This architecture enables multiple desktop environments to run securely on the same host machine.

---

## Design Philosophy

Docinium is designed as both:

- A developer-friendly Python orchestration library
- A browser-based remote desktop platform

The system combines infrastructure orchestration with accessible browser interaction to simplify management of distributed desktop environments.

Its architecture makes it suitable for:

- Remote desktop infrastructure
- Automation systems
- Educational labs
- Accessibility-focused computing
- Multi-user desktop platforms
- Browser-based development environments

--- 