# Copyright (c) 2023 kyasuda (GitHub: @KYasuda516)
# This software is released under the MIT License, see LICENSE.

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="mylib",
  version="0.0.1",
  install_requires=[
    "logging",
    "pathlib",
    "csv",
    "typing",
    "json",
    "subprocess",
    "datetime",
    "re",
  ],
  author="kyasuda",
  # author_email="",
  license='MIT',
  description="You can utilize kyasuda's applications.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/KYasuda516/python-mylib",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  packages=setuptools.find_packages(),
  python_requires=">=3.8",
)
