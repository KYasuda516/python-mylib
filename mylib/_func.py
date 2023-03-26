# Copyright (c) 2023 Kanta Yasuda (GitHub: @KYasuda516)
# This software is released under the MIT License, see LICENSE.

def list2unique_list(l: list) -> list:
  return (sorted(set(l), key=l.index))
