# Copyright (c) 2023 Kanta Yasuda (GitHub: @kyasuda516)
# This software is released under the MIT License, see LICENSE.

import json as __json
import typing as __typing
from pathlib import Path as __Path

def load(path: __Path) -> __typing.Any:
  with open(path.as_posix(), 'r') as f:
    d = __json.load(f)
  return d

def dump(data: __typing.Any, path: __Path):
  with open(path.as_posix(), 'w') as f:
    __json.dump(data, f, indent=2)


class JsonData():
  from pathlib import Path as __Path
  def __init__(self, path: __Path):
    self.__path = path
    self.__data = load(self.__path)
  
  def get(self, key: str) -> object:
    return self.__data[key]

  def set(self, key: str, value: object):
    self.__data[key] = value
    dump(self.__data, self.__path)

  def delete(self, key: str, missing_ok=True):
    if key in self.__data:
      del self.__data[key]
      dump(self.__data, self.__path)
    else:
      if not missing_ok:
        raise KeyError(key)
