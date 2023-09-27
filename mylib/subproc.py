# Copyright (c) 2023 Kanta Yasuda (GitHub: @kyasuda516)
# This software is released under the MIT License, see LICENSE.

import subprocess as __sp
from typing import List as __List

def run(*commands) -> str:
  """subprocess.run()を簡単に実行するための関数
  
  失敗すれば例外（単なるException）を吐く
  """

  # 注意：この関数はmylib.path.open_dir_for_temp()から依存されている
  proc = __sp.run(commands, shell=True, stdout=__sp.PIPE, stderr=__sp.STDOUT)
  if proc.returncode != 0:
    raise Exception(proc.stdout.decode('shift-jis'))
  stdout = proc.stdout.decode('shift-jis')
  return stdout

def Popen(*commands) -> None:
  """subprocess.Popen()を簡単に実行するための関数"""

  proc = __sp.Popen(commands, shell=True, stdout=__sp.PIPE, stderr=__sp.STDOUT)
