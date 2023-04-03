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

def mkdir_empty(path: __Path, exist_ok: bool=False):
  """空のディレクトリを作成
  
  path: 対象のディレクトリのパス
  exist_ok: Trueにすると、pathがディレクトリまたはファイルとして存在していた場合、
  それを削除したうえで作成する。
  """

  if not path.exists():
    path.mkdir(parents=True)
  if not exist_ok:
    FileExistsError(
      f'Cannot create a file when that file already exists: {path.as_posix()}'
      )
  if path.is_dir():
    import shutil
    shutil.rmtree(path.as_posix())
  else:
    path.unlink()
  path.mkdir(parents=True)

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
      if comp[0]=='.' and not comp in ('.', '..')
    ]

  # Unixマシンの場合
  if isinstance(path, PosixPath):
    comps = [
      comp.replace(':', new_char)
      for comp in comps
    ]

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
      if comp[-1]=='.' and not comp in ('.', '..')
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

def avoid_overwrite(path: __Path, is_dir=False) -> __Path:
  """ファイルやディレクトリが既に存在する場合に、数字を付け加えることで上書きを回避
  
  path: 対象のパス
  is_dir: 対象のパスをディレクトリと想定している場合Trueにする
  """

  if not path.exists(): return path
  n = 1
  while True:
    new_path = path.with_name(f'{path.name} ({n})') \
      if is_dir \
      else path.with_stem(f'{path.stem} ({n})')
    if not new_path.exists(): return new_path
    n += 1

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

