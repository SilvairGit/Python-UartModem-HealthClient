from setuptools import setup, find_packages

setup(
    name="silvair_health_client",
    version="2.8.0",
    author="Silvair",
    author_email="support@silvair.com",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.6.0",
    install_requires=[
        "silvair-uart-common-libs==2.8.0",
        "silvair-otau-demo==2.8.0",
        "nose"
    ],
    dependency_links = [
      "git+https://github.com/SilvairGit/Python-UartModem-Common.git@2.8.0#egg=silvair-uart-common-libs-2.8.0",
      "git+https://github.com/SilvairGit/Python-UartModem-OTAU.git@2.8.0#egg=silvair-otau-demo-2.8.0"
    ]
)
