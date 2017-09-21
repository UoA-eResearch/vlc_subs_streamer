#!/usr/bin/python
import sys
import srt
import time
import telnetlib
import re
import os

def get_file():
  t.write("status\n")
  r = t.read_until(">")
  if "file" not in r:
    return None
  m = re.search(r'//(.+?) \)', r)
  return m.group(1)

def get_time():
  t.write("get_time\n")
  s = t.read_until(">").split("\n")[0].strip()
  if not s:
    return 0
  s = int(s)
  return s

t = telnetlib.Telnet("localhost", 4212)
t.read_until("Password: ")
t.write("admin\n")
t.read_until(">")

print("connected to vlc")

last_file = None
last_sub = ""

while True:
  filename = get_file()
  if not filename:
    continue
  if filename != last_file:
    filename_wo_ext = os.path.splitext(filename)[0]
    srt_file = filename_wo_ext + ".srt"
    print("Reading {}".format(srt_file))
    try:
      with open(srt_file) as f:
        subs = list(srt.parse(f.read()))
    except Exception as e:
      subs = []
      print(e)
    last_file = filename

  pos = get_time()
  for sub in subs:
    if pos >= sub.start.total_seconds() and pos <= sub.end.total_seconds() and sub != last_sub:
      last_sub = sub
      print(sub.content)
  time.sleep(.1)
