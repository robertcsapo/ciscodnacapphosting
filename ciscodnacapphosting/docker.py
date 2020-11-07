import docker


class Api:
    def __init__(self):
        self.docker_client = docker.from_env()
        return

    def download(self, image=None, tag="latest"):
        if image is None:
            raise Exception(f"Error (download): Docker image name missing ({image})")
        #print(self.docker_client)
        images = self.docker_client.images.list()
        #print(images)
        pull = self.docker_client.images.pull(image, tag)
        print(pull)
        return

    def save(self, image=None, tag="latest"):
        if image is None:
            raise Exception(f"Error (save): Docker image name missing ({image})")
        tar = self.docker_client.images.get(f"{image}:{tag}")
        f = open(f'./{image}_{tag}.tar', 'wb')
        for chunk in tar.save():
            f.write(chunk)
        f.close()
        return