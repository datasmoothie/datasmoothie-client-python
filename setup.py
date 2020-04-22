import setuptools


setuptools.setup(
    name="datasmoothie",
    packages=['datasmoothie'],
    extras_require={':python_version<"3.7"': ['importlib-resources']},
    version="0.7",
    license='MIT',
    url="https://github.com/datasmoothie/datasmoothie-client-python",
    download_url="https://github.com/datasmoothie/datasmoothie-client-python/archive/v0.7.tar.gz",
    author="Geir Freysson",
    author_email="geir@datasmoothie.com",
    description="Python wrapper for v2 of the Datasmoothie API.",
    keywords=['surveys', 'market research', 'weighting', 'significance tests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
