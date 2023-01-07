import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dflow-phonon",
    version="0.0.12",
    author="Chengqian Zhang",
    author_email="2043899742@qq.com",
    description="A phonon calculation package based on dflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chengqian-Zhang/dflow-phonon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    provides=["dflowphonon"],
    scripts=["scripts/dflowphonon"]
)
