import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .logger_config import logger


class GuacamoleClient:
    def __init__(
        self,
        url="http://localhost:8080",
        username="guacadmin",
        password="guacadmin",
        timeout=5,
    ):
        self.url = url.rstrip("/")
        self.username = username
        self.password = password
        self.timeout = timeout

        self.token = None
        self.datasource = None

        # ---- create ONE session ----
        self.session = requests.Session()

        # ---- retries ----
        retries = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self._login()

    def _login(self):
        login_url = f"{self.url}/api/tokens"

        data = {
            "username": self.username,
            "password": self.password,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        }

        try:
            response = self.session.post(
                login_url,
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError(
                f"Cannot connect to Guacamole at {self.url}. "
                f"Is the server running and port exposed?"
            ) from e

        # logger.debug(response.text)
        response.raise_for_status()

        json_resp = response.json()

        self.token = json_resp.get("authToken")
        self.datasource = json_resp.get("dataSource")

        if not self.token or not self.datasource:
            raise ValueError(
                "Failed to obtain authToken or dataSource from Guacamole API"
            )

        # ---- attach token globally ----
        self.session.headers.update(
            {
                "Guacamole-Token": self.token,
                "Accept": "application/json",
            }
        )

    def list_all_users(self):
        users_url = f"{self.url}/api/session/data/{self.datasource}/users"
        # logger.warning(users_url)
        response = self.session.get(users_url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
