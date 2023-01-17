#!/usr/bin/env python3

import sys
import tarfile
import os
from time import time
from datetime import datetime

backup_path = '/backups'
base_path = '/data'

files = [os.path.join(base_path, f) for f in os.listdir(backup_path) if f.endswith('.tar.bz2')]
now_abs = time()
now_dt = datetime.now()
now_weekday = now_dt.weekday()
now_h = now_dt.hour
DELTA_DAY = 60 * 60 * 24
N_KEEP = 5

if now_weekday != 5:
    # only backup on saturday
    print(f"Only backup on saturdays (=5), its {now_weekday}")
    sys.exit(0)

if now_h < 3 or now_h > 5:
    # only start between 3 and 5
    print(f"Only backup between 3 and 5, its {now_h}")
    sys.exit(0)

if any([now_abs - os.path.getctime(f) < 3 * DELTA_DAY for f in files]):
    print(f"There was a backup not too long ago")
    sys.exit(0)

time_format = "%Y-%m-%d_%H:%M:%S"
backup_file_name = f"nc_backup_{now_dt.strftime(time_format)}.tar.bz2"
print(f"Backing up now to {backup_file_name} ...", end='')
with tarfile.open(os.path.join(backup_path, backup_file_name), "W:bz2") as tar:
    tar.add(base_path)
print(f"done")
