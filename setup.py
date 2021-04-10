from os import path
from setuptools import setup, find_packages
import ciscodnacapphosting

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


# pwd = path.abspath(path.dirname(__file__))
with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name="ciscodnacapphosting",
    author=ciscodnacapphosting.author,
    author_email=ciscodnacapphosting.email,
    description=ciscodnacapphosting.description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=ciscodnacapphosting.repo_url,
    version=ciscodnacapphosting.version,
    packages=find_packages(),
    py_modules=["ciscodnacapphosting"],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        ciscodnacapphosting=ciscodnacapphosting.cli:cli
        """,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "License :: Other/Proprietary License",
    ],
    license=ciscodnacapphosting.license,
    python_requires=">=3.8",
)
