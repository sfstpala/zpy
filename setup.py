import setuptools


setuptools.setup(
    name="zpy", version="0.0.0",
    description="quickly encrypt files with your ssh identity",
    packages=setuptools.find_packages(),
    test_suite="zpy.tests",
    author="Stefano Palazzo",
    author_email="stefano.palazzo@gmail.com",
    url="https://github.com/sfstpala/zpy",
    zip_safe=False,
    install_requires=[
        "docopt",
        "pycrypto",
    ],
    entry_points={
        "console_scripts": [
            "zpy = zpy.__main__:main",
        ]
    },
)
