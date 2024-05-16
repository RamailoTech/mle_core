from setuptools import setup, find_packages

def parse_requirements(filename):
    """ Load requirements from a pip requirements file """
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line and not line.startswith('#')]


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mle_core",
    version="0.1.0",
    author="ML Experts Team",
    author_email="mlexperts@example.com",
    description="Core modules necessary during application development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RamailoTech/mle_core",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=parse_requirements('requirements.txt'),
    include_package_data=True,
)
