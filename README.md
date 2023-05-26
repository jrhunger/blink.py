# blink.py - cli tool for blinkpy
Uses and requires [fronzbot/blinkpy](https://github.com/fronzbot/blinkpy), exposing functionality by command-line arguments.

## setup
### install/download blinkpy
Night-vision control requires at least version 0.21.0.rc0, (see [releases](https://github.com/fronzbot/blinkpy/releases)) which is not available from pip.  
Download and extract to blinkpy/ in the same place where blink.py is

After the next release, you can install with "pip install blinkpy"

### create .auth file in same dir
Format is:
```
{"username": "user@domain.tld", "password": "S3cret-St0.ff"}
```

## usage
blink.py [-h] (--arm | --disarm | --nv {off,on,auto} | --status | --snap) [--camera CAMERA] [--snapdir SNAPDIR]
* at least one of the arguments in parenthesis is required
  * --arm and --disarm do what they say
  * --nv sets the night-vision to off, on, or auto per the argument
  * --status shows the current night-vision and arm status
  * --snap snaps a picture and saves to SNAPDIR (see below)
* --camera is optional and defaults to the first one returned when listing cameras
* --snapdir is optional and defaults to /data (i run it in docker and bind mount the real directory there)

