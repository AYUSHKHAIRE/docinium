import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .logger_config import logger

class GucamoleClient:
    def __init__(self, url="http://localhost:8080", username="guacadmin", password="guacadmin"):
        self.url = url.rstrip("/")
        self.username = username
        self.password = password
        self.token = None
        self.datasource = None
        self.session = requests.Session()  # persistent session

        # Retry configuration
        retries = Retry(
            total=5,                  # number of total retries
            backoff_factor=0.5,       # exponential backoff (0.5s, 1s, 2s…)
            status_forcelist=[502, 503, 504],  # retry on these HTTP statuses
            allowed_methods=["GET", "POST"]    # retry for GET and POST requests
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Headers copied from browser
        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": self.url,
            "Referer": self.url + "/",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        })

        self._login()

    def _login(self):
        login_url = f"{self.url}/api/tokens"
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.session.post(login_url, data=data)
        logger.debug(response.text)
        response.raise_for_status()
        json_resp = response.json()
        self.token = json_resp.get("authToken")
        self.datasource = json_resp.get("availableDataSources")[0]

        if not self.token or not self.datasource:
            raise ValueError("Failed to obtain authToken or datasource from Guacamole API")

        # Set cookie for future requests
        self.session.cookies.set("GUAC_AUTH", self.token)

    def list_all_users(self):
        users_url = f"{self.url}/api/session/data/{self.datasource}/users"
        # Explicitly include the Authorization header with Bearer token
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        # Use the session with cookie + Authorization header
        response = self.session.get(users_url, headers=headers)
        response.raise_for_status()
        return response.json()