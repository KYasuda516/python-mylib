# Copyright (c) 2023 kyasuda (GitHub: @KYasuda516)
# This software is released under the MIT License, see LICENSE.
import datetime

def get_timecode() -> str:
  dt = datetime.datetime.now()
  tc =  f'{dt.year}{dt.month}{dt.day}{dt.hour}{dt.minute}{dt.second}'
  return tc
