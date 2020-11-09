import logging
import docker


class Api:
    def __init__(self):
        self.docker_client = docker.from_env()
        return

    def download(self, image=None, tag="latest"):
        if image is None:
            raise Exception(f"Error (download): Docker image name missing ({image})")
        logging.info(f"Docker downloading {image}:{tag}")
        download = self.docker_client.images.pull(image, tag)
        data = {"image": image, "tag": tag}
        return data

    def save(self, image=None, tag="latest"):
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
