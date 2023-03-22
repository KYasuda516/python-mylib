# Copyright (c) 2023 kyasuda (GitHub: @KYasuda516)
# This software is released under the MIT License, see LICENSE.

import csv as __csv
import typing as __typing
from contextlib import contextmanager as __contextmanager
from os import PathLike as __PathLike
from io import StringIO as __StringIO

@__contextmanager
def open_mode_rt(
  filepath_or_buffer: __typing.Union[str, bytes, __PathLike, __StringIO], 
  **kwargs
  ) -> __typing.Any:
  """バッファも受け付ける、テキストファイル読み取り専用のopen()関数。

  ※with文で使うこと。
  """

  is_path = False
  if isinstance(filepath_or_buffer, (str, bytes, __PathLike)):
    is_path = True
    f = open(filepath_or_buffer, mode="rt", **kwargs)
  elif isinstance(filepath_or_buffer, __StringIO):
    f = filepath_or_buffer
  else:
    raise TypeError(
      "expected str, bytes, os.PathLike object, StringIO or BytesIO, "
      f"not {type(filepath_or_buffer).__name__}")
  
  try:
    yield f
  finally:
    if is_path:
      f.close()
    else:
      f.seek(0)

def load_csv_data(
  filepath_or_buffer: __typing.Union[str, bytes, __PathLike, __StringIO], 
  *,
  encoding: str='UTF-8', 
  header: __typing.Union[None, __typing.Literal["infer"]]="infer"
  ) -> __typing.List[__typing.List[str]]:
  """CSVを読み込み、文字列を要素にもつ2次元リストとして返す。
  
  ボディに何も書いてなかったら[]を返す。
  また、たとえ1列のみでも、返されるのは2次元リスト。

  ソースとなるCSVに見出し行（1行）がない場合、header=None にしてください。
  """

  idx_std = 0
  if header=="infer":
    idx_std = 1
  elif header is None:
    pass
  else:
    raise ValueError('expected value is None or Literal "infer"')
  
  with open_mode_rt(filepath_or_buffer, newline='\n', encoding=encoding) as f:
    data = [row for idx, row in enumerate(__csv.reader(f)) if idx >= idx_std]
  if not data:
    return []
  if not data[0]:
    return []
  return data

def load_csv_data2(
  filepath_or_buffer: __typing.Union[str, bytes, __PathLike, __StringIO], 
  *,
  encoding: str='UTF-8'
  ) -> __typing.Dict[str, __typing.List[str]]:
  """見出し行のあるCSVを読み込み、リストの辞書を返す。
  
  見出し行は1行。
  見出しに対応するキーを擁する辞書を返す。
  辞書のバリューはリストで、一列のボディ部分。
  ボディに何も書いてなかったら辞書のバリューは[]となる。
  """
  
  with open_mode_rt(filepath_or_buffer, newline='\n', encoding=encoding) as f:
    rawdata = [row for row in __csv.reader(f)]
  if not rawdata: return {}
  idx_row = rawdata.pop(0)
  data = {col[0]: list(col[1:]) for col in zip(idx_row, *rawdata)}
  return data

def append_csv_data(
  filepath: __typing.Union[str, bytes, __PathLike], 
  new_row: __typing.List[str]
  ) -> None:
  """CSVファイルに1行追加する。"""

  with open(filepath, mode='a', newline='\n', encoding='UTF-8') as f:
    writer = __csv.writer(f)
    writer.writerow(new_row)

def update_csv_data(
  filepath: __typing.Union[str, bytes, __PathLike], 
  list2: __typing.List[__typing.List[str]], 
  *,
  header: __typing.Union[None, __typing.Literal["infer"]]="infer"
  ) -> None:
  """CSVファイルのボディを塗り替える。

  対象のCSVファイルに見出し行（1行）がない場合、header=None にしてください。
  """

  new_data = None
  if header is None:
    new_data = list2
  elif header=="infer":
    with open(filepath, mode='r', newline='\n', encoding='UTF-8') as f:
      for row in __csv.reader(f):
        data_index = row    #これは1次元
        break
    new_data = [data_index, *list2]
  else:
    raise ValueError('expected value is None or Literal "infer"')

  with open(filepath, mode='w', newline='\n', encoding='UTF-8') as f:
    writer = __csv.writer(f)
    writer.writerows(new_data)
