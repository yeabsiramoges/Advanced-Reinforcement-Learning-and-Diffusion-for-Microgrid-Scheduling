import os

from dotenv import load_dotenv
from setuptools import find_packages, setup

load_dotenv()

PROJECT_NAME = os.getenv("PROJECT_NAME")
PROJECT_VERSION = os.getenv("PROJECT_VERSION")


setup(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
    description="Adaptive Diffusion-based Reinforcement Learning",
    author="MIT EEGS Microgrid",
    author_email="eegs-microgrid@mit.edu",
    url="https://github.com/yeabsiramoges/Advanced-Reinforcement-Learning-and-Diffusion-for-Microgrid-Scheduling",
    package_data={"": ["rldiff"]},
    include_package_data=True,
    zip_safe=False,
    packages=find_packages("rldiff"),
    install_requires=["gymnasium", "matplotlib", "pandas"],
    extra_require={"dev": ["black", "pytest", "isort", "tox-conda"]},
    python_requires=">3.8",
)
