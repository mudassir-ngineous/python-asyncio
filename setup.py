from setuptools import setup, find_packages


setup(
    # Application name:
    name="algorithms",

    # Application author details:
    author="Mudassirkhan",
    author_email="mudassir@intangles.com",

    # Packages
    packages=find_packages(),

    # Include additional files into the package
    include_package_data=True,

    # Details

    # license="LICENSE.txt",
    description="Python AsyncIO ",
    classifiers=[
        "Programming Language :: Python 3.6.4 :: Anaconda, Inc",
        "Topic :: Algorithms :: Analytics"
    ],
    url="https://github.com/Intangles/algorithms",
    license="Open Source",


    # Dependent packages (distributions)
    install_requires=[
        "requests",
        "urllib3",
        "aiohttp",
        "async_timeout",
        "aioredis",
        "motor",
        "aiofiles",
        "bokeh"
    ],
)