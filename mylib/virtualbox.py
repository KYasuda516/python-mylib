# Copyright (c) 2023 Kanta Yasuda (GitHub: @kyasuda516)
# This software is released under the MIT License, see LICENSE.

import re as __re
from typing import List as __List
from pathlib import Path as __Path
from mylib import subproc as __sp
P_VBOX_MANAGE = __Path("C:/Program Files/Oracle/VirtualBox/VBoxManage.exe")

def get_vm_list() -> __List[str]:
  global P_VBOX_MANAGE
  res = __sp.run_proccess([P_VBOX_MANAGE.as_posix(), "list", "vms"])
  regexp = '\n".+" '   # 行頭(^)は1行の先頭ではなく文字列の先頭という意味になったので。。
  l = [s[2:-2] for s in __re.findall(regexp, f'\n{res}')]   # 先頭と末尾の不要なものを削除
  return l

def is_running(vm_name: str) -> bool:
  global P_VBOX_MANAGE
  res = __sp.run_proccess([P_VBOX_MANAGE.as_posix(), "list", "runningvms"])
  regexp = f'\n"{vm_name}" '   # 行頭(^)は1行の先頭ではなく文字列の先頭という意味になったので。。
  b = bool(__re.search(regexp, f'\n{res}'))
  return b

def run_vm(vm_name: str, running_ok: bool=True):
  global P_VBOX_MANAGE
  if not vm_name in get_vm_list():
    raise Exception(f'仮想マシン {vm_name} が見つかりません。')
  if is_running(vm_name):
    if not running_ok:
      raise Exception(f'仮想マシン {vm_name} はすでに起動しています。')
  else:
    res = __sp.run_proccess([P_VBOX_MANAGE.as_posix(), "startvm", vm_name, "--type", "headless"])
    import time
    time.sleep(1)

def poweroff_vm(vm_name: str):
  global P_VBOX_MANAGE
  if not vm_name in get_vm_list():
    raise Exception(f'仮想マシン {vm_name} が見つかりません。')
  if is_running(vm_name):
    res = __sp.run_proccess([P_VBOX_MANAGE.as_posix(), "controlvm", vm_name, "poweroff"])

