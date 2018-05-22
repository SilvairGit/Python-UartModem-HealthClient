from setuptools import setup, find_packages

setup(
    name="silvair_health_client",
    version="0.0.1",
    author="Silvair",
    author_email="support@silvair.com",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.6.0",
    install_requires=[
        "silvair-uart-common-libs==0.0.1",
        "silvair-otau-demo==0.0.1",
        "nose"
    ],
    dependency_links = [
      "git+https://github.com/SilvairGit/Python-UartModem-Common.git#egg=silvair-uart-common-libs-0.0.1",
      "git+https://github.com/SilvairGit/Python-UartModem-OTAU.git#egg=silvair-otau-demo-0.0.1"
    ]
)