#!/usr/bin/python
import sys
import srt
import time
import telnetlib
import re
import os
from socket import *

ips = ["172.22.0.80", "172.22.0.81", "172.22.0.82"]

def broadcast(msg, port=15000):
  for ip in ips:
    s.sendto(msg.encode("utf-8"), (ip, port))
  s.sendto(msg.encode("utf-8"), ('<broadcast>', port))

def get_file():
  t.write("status\n".encode("utf-8"))
  r = t.read_until(">".encode("utf-8")).decode("utf-8")
  if "file" not in r:
    return None
  m = re.search(r'//(.+?) \)', r)
  return m.group(1)

def get_time():
  t.write("get_time\n".encode("utf-8"))
  s = t.read_until(">".encode("utf-8")).decode("utf-8").split("\n")[0].strip()
  if not s:
    return 0
  s = int(s)
  return s

# Setup VLC telnet
t = telnetlib.Telnet("localhost", 4212)
t.read_until("Password: ".encode("utf-8"))
t.write("admin\n".encode("utf-8"))
t.read_until(">".encode("utf-8"))

print("connected to vlc")

# Setup UDP broadcast socket
s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

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
    if pos >= sub.start.total_seconds() and pos <= sub.end.total_seconds() and sub.content != last_sub:
      last_sub = sub.content
      print(sub.content)
      broadcast(sub.content)
  time.sleep(.1)
