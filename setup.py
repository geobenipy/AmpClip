from setuptools import setup

setup(
    name="ampclip",
    version="1.0.0",
    description="Prestack SEG-Y Amplitude Threshold Muting Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Beni",
    py_modules=["ampclip"],
    python_requires=">=3.8",
    install_requires=[
        "segyio>=1.9.0",
        "numpy>=1.21.0",
        "tqdm>=4.62.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
