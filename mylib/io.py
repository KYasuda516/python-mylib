# Copyright (c) 2023 Kanta Yasuda (GitHub: @kyasuda516)
# This software is released under the MIT License, see LICENSE.

import typing as __typing
from pathlib import Path as __Path

def yes_no_input(message: str) -> bool:
  while True:
    choice = input(f"{message} ([y]/N): ").lower()
    if choice in ('y', 'ye', 'yes'):
      return True
    elif choice in ('n', 'no'):
      return False

def num_input(message: str, start: int, stop: int) -> int:
  print(message)
  nums = list(range(start, stop))
  while True:
    choice = input(f'Prease choose from {start} to {stop-1}: ')
    try:
      num = int(choice)
      if num in nums:
        return num
    except:
      pass

def num_input2(question: str, d_msg: dict, msg_bef: str='', msg_aft: str='') -> __typing.Any:
  keys = list(d_msg.keys())
  msg = f'{question}\n'
  for idx, key in enumerate(keys):
    msg = f'{msg}{idx: 3}\t{msg_bef}{d_msg[key]}{msg_aft}\n'
  msg = msg[:-1]  # 最後の改行を取っ払う
  idx = num_input(msg, 0, len(keys))
  key = keys[idx]
  return key

def blank_ng_input(message: str) -> str:
  while True:
    choice = input(message).strip()
    if choice != '':
      return choice

def fpath_existing_input(message: str, ext: str=None) -> __Path:
  while True:
    p = __Path(input(message).strip().replace('"', ''))
    if (ext is None or p.suffix==ext) and p.exists():
      return p

class Outputter():
  # ファイルに出力したいが、マクロを実行する以前に書いてあった内容は削除したいというときに使う。
  # たとえば、lyric_assistにて、歌詞をtemptxtに書き出すのに用いてる。
  from pathlib import Path as __Path  #なぜか要る。。
  def __init__(self, txt_path: __Path):
    self.txt_path = txt_path
    with open(self.txt_path.as_posix(), 'w') as f:
      f.write('')
  
  def output(self, msg: str):
    with open(self.txt_path.as_posix(), 'a') as f:
      f.write(msg)
