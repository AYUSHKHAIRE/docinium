import requests
import json
from .logger_config import logger

def register_rdp_connection(
    container_connected_name: str,
    identifier: int,
    auth_token: str,
    guacamole_token: str,
    base_url: str
):
    url = f"{base_url}/connector/api/rdp-connection/{container_connected_name}/{identifier}/{guacamole_token}/"
    headers = {
        "Authorization": f"Token {auth_token}"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to register RDP connection: {response.text}")