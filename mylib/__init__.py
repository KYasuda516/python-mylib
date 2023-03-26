# Copyright (c) 2023 Kanta Yasuda (GitHub: @KYasuda516)
# This software is released under the MIT License, see LICENSE.

from mylib import csv
from mylib import json
from mylib import path
from mylib import io
from mylib import subproc
from mylib import time
from mylib import util
from mylib import virtualbox
from mylib import subproc
from mylib import *

from mylib._func import *
from mylib._const import *

import logging
# 出力フォーマットについての詳細は
# https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
logging.basicConfig(
  level=logging.INFO, 
  filename=P_LOG.as_posix(), 
  filemode='a', 
  encoding='UTF-8', 
  format='[%(process)d] %(asctime)s %(filename)s - %(levelname)s - %(message)s'
  )
