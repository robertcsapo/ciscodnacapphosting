from setuptools import setup, find_packages
import ciscodnacapphosting

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="ciscodnacapphosting",
    author=ciscodnacapphosting.author,
    description=ciscodnacapphosting.description,
    version=ciscodnacapphosting.version,
    packages=find_packages(),
    py_modules=["ciscodnacapphosting"],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        ciscodnacapphosting=ciscodnacapphosting.cli:cli
    """,
    python_requires=">=3.8",
)
