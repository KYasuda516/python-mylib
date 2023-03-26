# Copyright (c) 2023 Kanta Yasuda (GitHub: @KYasuda516)
# This software is released under the MIT License, see LICENSE.

import setuptools

# パッケージ名
NAME = "mylib"

# バージョンの読み込み
ver = {}
with open(f"{NAME}/__version__.py", "r", encoding="utf-8") as f:
  exec(f.read(), ver)

# READMEの読み込み
with open("README.md", "r", encoding="utf-8") as f:
  long_description = f.read()

setuptools.setup(
  packages=setuptools.find_packages(),
  name=NAME,
  version=ver.get("__version__"),
  author="kyasuda",
  url="https://github.com/KYasuda516/python-mylib",
  description="You can utilize kyasuda's applications.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  license='MIT',
  install_requires=[],
  python_requires=">=3.8",
)
