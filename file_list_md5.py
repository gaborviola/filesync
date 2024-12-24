#!/usr/bin/env python
import sys
import os
import subprocess
import datetime

if len(sys.argv)==3:
    sys.stdout.reconfigure(encoding=sys.argv[2])

if os.name == 'nt':
    cmd = [3, 'CertUtil', '-hashfile', '', 'MD5']
    decode = lambda x: x.split('\n')[1].strip()
else:
    cmd = [2, 'md5sum', '']
    decode = lambda x: x.split(' ')[0]

rootdir = os.getcwd() if len(sys.argv)==1 else sys.argv[1]

def float2strdate(floatin):
  return datetime.datetime.fromtimestamp(floatin).isoformat(sep=' ', timespec='seconds')

subdir_ex=''
for subdir, dirs, files in os.walk(rootdir):
    if subdir != subdir_ex:
        print('.'+subdir[len(rootdir):].replace('\\', '/'))
        subdir_ex=subdir
    #for file in os.listdir(subdir):
    for file in files:
        fname=os.path.join(subdir, file)
        size = os.path.getsize(fname)
        mtime = float2strdate(os.path.getmtime(fname))
        ctime = float2strdate(os.path.getctime(fname))
        if size:
            cmd[cmd[0]]=fname
            result = subprocess.run(cmd[1:], capture_output=True, text=True)
            md5 = decode(result.stdout)
        else:
            md5=''
        print(f'\t{file}\t{md5}\t{size}\t{ctime}\t{mtime}')
