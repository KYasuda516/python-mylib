# Copyright (c) 2023 kyasuda (GitHub: @KYasuda516)
# This software is released under the MIT License, see LICENSE.

def str2bool(s: str) -> bool:
  l = ["False", "None", "''", '""', "[]", "{}", "()"]
  if s in l:
    return False
  else:
    try:
      return False if float(s) == 0.0 else True
    except:
      return True
