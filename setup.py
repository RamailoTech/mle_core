from setuptools import setup, find_packages
import os 

def parse_requirements(requirements_filename, exclude_filename=None):
    """ Load requirements from a pip requirements file and optionally exclude certain packages """
    
    # Read requirements from the specified file
    with open(requirements_filename, 'r') as file:
        lines = file.readlines()
    
    # If an exclusion file is specified, load the exclusions
    exclusions = []
    if exclude_filename and os.path.isfile(exclude_filename):
        with open(exclude_filename, 'r') as file:
            exclusions = [line.strip() for line in file.readlines() if line.strip()]
    
    # Filter out any lines that should be excluded or are comments/blank
    return [
        line.strip() for line in lines
        if line.strip() and not line.startswith('#') and all(exclusion not in line for exclusion in exclusions)
    ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mle_core",
    version="0.1.0",
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
    install_requires=parse_requirements('requirements.txt', 'exclude_requirements.txt'),
    include_package_data=True,
)
