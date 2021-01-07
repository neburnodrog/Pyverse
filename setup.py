import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="pyverse",
    version="1.0.0",
    description="find syllables and rhymes of words/verses in spanish",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/neburnodrog/Pyverso",
    author="Ruben Karlsson",
    author_email="neburnodrog@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["pyverse"],
    install_requires=[
        "Click==7.1.2",
        "numlet"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pyverse=pyverse.__main__:silabify",
        ]
    },

)
