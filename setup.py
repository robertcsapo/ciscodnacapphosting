from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="ciscodnacapphosting",
    author="Robert Csapo",
    author_email="rcsapo@cisco.com",
    description="Cisco DNA Center App Hosting SDK",
    version="0.0.4",
    packages=find_packages(),
    py_modules=["ciscodnacapphosting"],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        ciscodnacapphosting=ciscodnacapphosting.cli:cli
    """,
    python_requires=">=3.8",
)
