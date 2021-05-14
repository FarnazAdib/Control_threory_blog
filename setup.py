import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Control_Theory_Blog",
    version="0.0.1",
    author="Farnaz Adib Yaghmaie",
    author_email="farnaz.adib.yaghmaei@gmail.com",
    description="A bloc for basic concepts in control theory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FarnazAdib/Control_threory_blog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)