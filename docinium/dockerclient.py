import docker 
from .logger_config import logger

class DockerManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
            logger.info("[ docinium engine > dockerclient ] Docker client initialized successfully.")
        except Exception as e:
            logger.error(f"[ docinium engine > dockerclient ] Failed to initialize Docker client: {e}")
        self.running_containers = {}

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

    def pull_image(self, image_name):
        try:
            logger.info(f"[ docinium engine > dockerclient ] Pulling image '{image_name}'...")
            self.client.images.pull(image_name)
            logger.info(f"[ docinium engine > dockerclient ] Image '{image_name}' pulled successfully.")
            return True
        except Exception as e:
            logger.error(f"[ docinium engine > dockerclient ] Failed to pull image '{image_name}': {e}")

    def check_if_docker_network_exists(self, network_name):
        try:
            networks = self.client.networks.list(names=[network_name])
            if networks:
                logger.info(f"[ docinium engine > dockerclient ] Docker network '{network_name}' exists.")
                return True
            else:
                logger.info(f"[ docinium engine > dockerclient ] Docker network '{network_name}' does not exist.")
                return False
        except Exception as e:
            logger.error(f"[ docinium engine > dockerclient ] Error checking Docker network '{network_name}': {e}")
            return False

    def create_docker_network(self, network_name):
        try:
            if self.check_if_docker_network_exists(network_name):
                logger.info(f"[ docinium engine > dockerclient ] Docker network '{network_name}' already exists.")
                return self.client.networks.get(network_name)
            network = self.client.networks.create(network_name, driver="bridge")
            logger.info(f"[ docinium engine > dockerclient ] Docker network '{network_name}' created successfully.")
            return network
        except Exception as e:
            logger.error(f"[ docinium engine > dockerclient ] Failed to create Docker network '{network_name}': {e}")

    def spin_up_docker_container(
        self,
        image_name,
        container_name,
        network_name,
        port_map = {},
        volumes=None,
        environment=None,
        command=None,
        detach=True,
    ):
        try:
            logger.info(f"[ docinium engine > dockerclient ] Running container '{container_name}' from image '{image_name}'...")
            container = self.client.containers.run(
                image=image_name,
                name=container_name,
                network=network_name,
                ports=port_map,
                volumes=volumes,
                environment=environment,
                command=command,
                detach=detach,
            )
            self.running_containers[f"{container.id}_{container_name}"] = container
            logger.info(f"[ docinium engine > dockerclient ] Container '{container_name}' is running.")
            return container
        except Exception as e:
            logger.error(f"[ docinium engine > dockerclient ] Failed to run container '{container_name}': {e}")

    def delete_docker_container(self, container_name):
        try:
            container = self.client.containers.get(container_name)
            container.stop()
            container.remove()
            logger.info(f"[ docinium engine > dockerclient ] Container '{container_name}' stopped and removed successfully.")
        except Exception as e:
            logger.error(f"[ docinium engine > dockerclient ] Failed to delete container '{container_name}': {e}")