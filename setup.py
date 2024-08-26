from setuptools import setup, find_packages
import os 

def parse_requirements(requirements_filename):
    """ Load requirements from a pip requirements file and optionally exclude certain packages """
    
    # Read requirements from the specified file
    with open(requirements_filename, 'r') as file:
        lines = file.readlines()
    
    # Filter out any lines that should be excluded or are comments/blank
    return [
        line.strip() for line in lines
        if line.strip() and not line.startswith('#') 
    ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mle_core",
    version="0.0.3",
    author="ML Experts Team",
    author_email="mvp@ramailo.tech",
    description="Core modules necessary during application development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RamailoTech/mle_core",
    project_urls={
        "Homepage": "https://github.com/RamailoTech/mle_core",
        "Issues": "https://github.com/RamailoTech/mle_core/issues",
    },
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
