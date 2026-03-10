from setuptools import setup, find_packages

setup(
    name="aegis-proxy",
    version="0.1.0",
    description="The official Python SDK for AegisProxy: The AI Firewall",
    author="Aegis",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.23.0",
    ],
    python_requires=">=3.8",
)
