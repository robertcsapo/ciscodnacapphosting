import docker


class Api:
    def __init__(self):
        self.docker_client = docker.from_env()
        return

    def download(self, image=None, tag="latest"):
        if image is None:
            raise Exception(f"Error (download): Docker image name missing ({image})")
        images = self.docker_client.images.list()
        download = self.docker_client.images.pull(image, tag)
        data = {}
        image = download.attrs["RepoTags"][0].split(":")
        data["image"] = image[0]
        data["tag"] = image[1]
        return data

    def save(self, image=None, tag="latest"):
        if image is None:
            raise Exception(f"Error (save): Docker image name missing ({image})")
        tar = self.docker_client.images.get(f"{image}:{tag}")
        filename = f"{image}_{tag}.tar"
        f = open(filename, 'wb')
        for chunk in tar.save():
            f.write(chunk)
        f.close()
        data = {
            "image": image,
            "tag": tag,
            "filename": filename
        }
        return data