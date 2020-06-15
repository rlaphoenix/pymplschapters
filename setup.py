from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="pymplschapters",
    version="1.0.4",
    author="PHOENiX",
    author_email="rlaphoenix@pm.me",
    description="Extract chapters from a blu-ray mpls to a matroska recognized xml file",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/rlaPHOENiX/pymplschapters",
    packages=find_packages(),
    install_requires=["lxml>=4.4.1"],
    entry_points={"console_scripts": ["pymplschapters=pymplschapters.__init__:main"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
