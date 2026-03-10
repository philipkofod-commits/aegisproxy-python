from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aegis-proxy",
    version="0.1.0",
    description="The official Python SDK for AegisProxy: The Zero-Trust Firewall for Autonomous Agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AegisProxy",
    author_email="philipkofodnielsen@gmail.com",
    url="https://github.com/philipkofod/aegisproxy-python",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.23.0",
    ],
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="ai agents security firewall llm proxy",
)
