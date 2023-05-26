#!/usr/local/bin/python3
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
import json
import sys
import argparse
from datetime import datetime

dt_now = datetime.now().strftime("%Y%m%d-%H%M")
print("(" + dt_now + ")" + str(sys.argv))

try: 
  with open("/work/.auth", "r") as auth_f:
    credentials = json.loads(auth_f.read())
except FileNotFoundError:
  print('ERROR: .auth file not found. create with format: \'{"username": "user@domain.tld", "password": "pass"}\'')
  sys.exit(1)

parser = argparse.ArgumentParser(
  prog='blink.py',
  description='Control blink camera',
)
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('--arm', action='store_true')
action.add_argument('--disarm', action='store_true')
action.add_argument('--nv', choices=["off", "on", "auto"])
action.add_argument('--status', action='store_true')
action.add_argument('--snap', action='store_true')
parser.add_argument('--camera')
parser.add_argument('--snapdir')
args = parser.parse_args()

# should have good arguments, set up the blink
blink = Blink()
blink.auth = Auth(credentials, no_prompt=True)
blink.start()

if args.camera:
  camera_name = args.camera
else:
  camera_name = list(blink.cameras.keys())[0]
  print("camera not specified. defaulting to " + camera_name)

camera=blink.cameras[camera_name]
if not camera:
  print("unable to retrieve camera " + camera_name)
  sys.exit(1)


if args.arm:
  print("arm")
  camera.sync.arm = True
  blink.refresh()
  print(json.dumps(camera.sync.arm))
elif args.disarm:
  print("disarm")
  camera.sync.arm = False
  blink.refresh()
  print(json.dumps(camera.sync.arm))
elif args.nv:
  print("nv=" + args.nv)
  camera.night_vision = args.nv
  print(camera.night_vision)
elif args.status:
  blink.refresh()
  print('{"night_vision": %s, "arm": %s}' % (json.dumps(camera.night_vision), camera.sync.arm))
elif args.snap:
  camera.snap_picture()
  blink.refresh()
  if args.snapdir:
    snapdir = args.snapdir
  else:
    snapdir = '/data'
    print('--snapdir not specified, defaulting to ' + snapdir)
  snapfile = snapdir + '/' + datetime.now().strftime("%Y%m%d-%H%M") + ".jpg"
  print('saving snap to ' + snapfile)
  camera.image_to_file(snapfile)
else:  # if args defined correctly should never get here
  parser.print_help()
  sys.exit(1)
