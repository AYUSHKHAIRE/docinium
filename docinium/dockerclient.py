import docker 
from .logger_config import logger

class DockerManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
            logger.info("[ docinium engine > dockerclient ] Docker client initialized successfully.")
        except Exception as e:
            logger.error(f"[ docinium engine > dockerclient ] Failed to initialize Docker client: {e}")

    def check_if_image_exists(self, image_name):
        try:
            self.client.images.get(image_name)
            logger.info(f"[ docinium engine > dockerclient ] Image '{image_name}' exists.")
            return True
        except docker.errors.ImageNotFound:
            logger.info(f"[ docinium engine > dockerclient ] Image '{image_name}' does not exist.")
            return False
        except Exception as e:
            logger.error(f"[ docinium engine > dockerclient ] Error checking image '{image_name}': {e}")
            return False
