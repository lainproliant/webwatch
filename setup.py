from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="webwatch",
    version="0.0.1",
    description="A simple script to watch a webpage and email when it changes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lainproliant/webwatch",
    author="Lain Musgrove (lainproliant)",
    author_email="lain.proliant@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="web scraper",
    packages=find_packages(),
    install_requires=["requests", "bs4"],
    extras_require={},
    package_data={'webwatch': []},
    data_files=[],
    entry_points={"console_scripts": ['webwatch=webwatch.script:main']},
)
