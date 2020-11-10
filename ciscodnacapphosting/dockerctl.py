""" Docker Class that integrates with local docker environment """
import logging
import docker


class Api:
    """ API interface """

    def __init__(self):
        self.docker_client = docker.from_env()

    def download(self, image=None, tag="latest"):
        """ Download images from docker.io """
        if image is None:
            raise Exception(f"Error (download): Docker image name missing ({image})")
        logging.info(f"Docker downloading {image}:{tag}")
        download = self.docker_client.images.pull(image, tag)
        data = {"image": image, "tag": tag}

        return data

    def save(self, image=None, tag="latest"):
        """ Save images as tar files """
        if image is None:
            raise Exception(f"Error (save): Docker image name missing ({image})")
        logging.info(f"Docker saving {image}:{tag}")
        tar = self.docker_client.images.get(f"{image}:{tag}")

        filename = f"{image.replace('/', '_')}-{tag}.tar"
        f = open(filename, "wb")
        for chunk in tar.save(named=True):
            f.write(chunk)
        f.close()

        data = {"image": image, "tag": tag, "filename": filename}

        return data
