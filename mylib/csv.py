# Copyright (c) 2023 kyasuda (GitHub: @KYasuda516)
# This software is released under the MIT License, see LICENSE.

import csv as __csv
import typing as __typing
from pathlib import Path as __Path

def load_csv_data(path: __Path, encoding: str='UTF-8', contains_index: bool=False) -> __typing.List[tuple]:    # ボディ部分だけ返す（見出しを含まない）。ボディに何も書いてなかったら[]を返す。
  idx_std = 0 if contains_index else 1
  with open(path.as_posix(), newline='\n', encoding=encoding) as f:
    data = [tuple(row) for idx, row in enumerate(__csv.reader(f)) if idx >= idx_std]      
    #要素タプルだよ！！注意。(utanet_crawlscrape.pyには何ら影響なし)　ただし1列のみの場合、あとで文字列にする。
  if not data:
    return []
  if not data[0]:
    return []
  if len(data[0]) == 1:
    data = [str(row[0]) for row in data]
  return data

def append_csv_data(path: __Path, t: tuple):    # タプルはもちろん1次元。
  with open(path.as_posix(), 'a', newline='\n', encoding='UTF-8') as f:
    writer = __csv.writer(f)
    writer.writerow(t)

def update_csv_data(path: __Path, list2: __typing.List[tuple], contains_index: bool=False):
  new_data = None
  if contains_index:
    new_data = list2
  else:
    with open(path.as_posix(), newline='\n', encoding='UTF-8') as f:
      for row in __csv.reader(f):
        data_index = tuple(row)    #これは1次元
        break
    new_data = [data_index, *list2]

  with open(path.as_posix(), 'w', newline='\n', encoding='UTF-8') as f:
    writer = __csv.writer(f)
    writer.writerows(new_data)
