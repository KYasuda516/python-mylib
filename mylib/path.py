# Copyright (c) 2023 Kanta Yasuda (GitHub: @kyasuda516)
# This software is released under the MIT License, see LICENSE.

from pathlib import Path as __Path

def create_temp_path(ext: str) -> __Path:
  """拡張子つきで一時ファイルのパスを作成して返す。
  
  extにはピリオドつきの拡張子を渡す。
  """
  from tempfile import TemporaryFile
  with TemporaryFile() as fp:
    stem = fp.name
  newpath = __Path(f'{stem}{ext}')
  return newpath

def copy_as_temp(path: __Path) -> __Path:
  """拡張子つきで一時ファイルとしてコピーし、そのパスを返す。
  
  finallyで削除することを忘れずに!
  """
  import shutil
  newpath = create_temp_path(path.suffix)
  shutil.copy(path.as_posix(), newpath.as_posix())
  return newpath

def mkdir_empty(p: __Path):
  if p.exists():
    if p.is_dir():
      import shutil
      shutil.rmtree(p.as_posix())
    else:
      print(f'It has existed as a file.: {p.as_posix()}')
      exit()
  p.mkdir(parents=True)

def convert_suffix(path: __Path, suffix: str, post_stem: str='', replace_file: bool=False) -> __Path:
  from .time import get_timecode
  # replace_fileがFalseの場合、ファイルが存在していればタイムコードをつけることで上書きを防ぐが、
  # replace_fileがTrueの場合、ファイルが存在していても上書きしてしまう。
  p = path.with_name(f'{path.stem}{post_stem}{suffix}')
  if not replace_file and p.exists():
    p = p.with_name(f'{p.stem}_{get_timecode}{p.suffix}')  # {get_timecode()}
    print(p)
  return p

def open_dir_for_temp():
  from . import subproc
  from tempfile import gettempdir
  stdout = subproc.run_proccess(['start', gettempdir()])
  print(stdout)

def postfix_stem(path: __Path, post_stem: str, replace_file: bool=False) -> __Path:
  p = convert_suffix(path=path, suffix=path.suffix, post_stem=post_stem, replace_file=replace_file)
  return p

def fix_path(
    path: __Path, 
    pre_period: bool=True,
    new_char: str='_'
    ) -> __Path:
  """不正なパスを修正

  OSによって禁止されているファイル・ディレクトリ名があるので、
  それを修正してパスとして返す。

  - path: ファイルまたはディレクトリのパス
  - pre_period: 先頭の `.` を許可するかどうか。False にすると先頭の `.` は置換される。
  - new_char: 不当な文字を用いていた場合、それを何に置換するか。
  """

  from pathlib import PosixPath, WindowsPath
  comps = list(path.parts)
  
  # 先頭のピリオドが許可されていない場合、置換
  if not pre_period:
    comps = [
      new_char + comp[1:]
      for comp in comps
      if comp[0]=='.'
    ]

  # Unixマシンの場合
  if isinstance(path, PosixPath):
    comps = map(str.replace(':', new_char), comps)

  # Windowsの場合
  if isinstance(path, WindowsPath):
    import re
    # 不正な文字を置換
    comps = [
      re.sub(r'[\:\*\?"\<\>\|\n\r\t\v]', new_char, comp)
      if not (i==0 and re.compile(r'[a-zA-Z]\:\\').fullmatch(comp))
      else comp
      for i, comp in enumerate(comps)
    ]
    # 末尾のピリオドを置換
    comps = [
      comp[:-1] + new_char
      if comp[-1]=='.'
      else comp
      for comp in comps
    ]
    # 予約語はステム末尾に文字を付加する
    comps = [
      re.sub(
        r'^(aux|con|nul|prn|com\d|lpt\d)',
        f'\\1{new_char}',
        comp,
        flags=re.IGNORECASE
      )
      if re.fullmatch(
        r'(aux|con|nul|prn|com\d|lpt\d)(\..+)?', 
        comp, 
        flags=re.IGNORECASE
      )
      else comp
      for comp in comps
    ]
  
  return __Path(*comps)

class TempDirPath(type(__Path())):  # これそのままPathを継承しようとしたらAttributeError: 'TempDirPath' object has no attribute '_flavour'というエラーに逢着するのでこうしている。
  """一時フォルダのパス
  
  インスタンスを作成した段階で一時フォルダが作成される。
  そしてディストラクタによる削除の段階でフォルダじたいも中身ごと削除される。
  """
  
  from typing import Any as __Any
  def __new__(cls, **kwargs: __Any):
    temp_path = create_temp_path('')
    self = super().__new__(cls, temp_path.as_posix(), **kwargs)
    temp_path.mkdir()
    return self

  from pathlib import Path as __Path
  def move_contents(self, dir_path: __Path):
    """中身をまるごと別のディレクトリへと移動
    
    別ディレクトリに同名のファイルがあれば上書きされる。
    """
    import shutil
    for p in self.iterdir():
      shutil.move(p.as_posix(), (dir_path / p.name).as_posix())

  def empty(self):
    """フォルダを空にする"""
    import shutil
    shutil.rmtree(self.as_posix())
    self.mkdir()

  def __del__(self):
    import shutil
    shutil.rmtree(self.as_posix(), ignore_errors=True)  # 削除に失敗してもエラーにしない

