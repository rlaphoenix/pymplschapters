from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="pymplschapters",
    version="1.0.0",
    author="PRAGMA",
    author_email="pragma.exe@gmail.com",
    description="Extract chapters from a blu-ray mpls to a matroska recognized xml file",
    license='MIT',
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/imPRAGMA/pymplschapters",
    packages=find_packages(),
    install_requires=[
        'lxml>=4.4.1'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)