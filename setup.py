from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="wowhmm",
    version="0.1.4",
    description="Who owes whom how much money",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoonthegoon/wowhmm",
    packages=find_packages(),
    install_requires=[
        "pandas==2.2.2",
    ],
)
