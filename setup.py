import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="pyverso",
    version="1.0.0",
    description="find syllables and rhymes of words/verses in spanish",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/neburnodrog/silabizador",
    author="Ruben Karlsson",
    author_email="neburnodrog@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["pyverso"],
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "pyverso=pyverso.__main__:silabify",
        ]
    },
)
