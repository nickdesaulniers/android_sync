# android_sync
Sync files from Android device

## Usage

```sh
$ ./sync.py [-h] [-v] source destination
```
```
positional arguments:
  source         Source file or directory
  destination    Destination directory on Android device

options:
  -h, --help     show this help message and exit
  -v, --verbose  Enable verbose output
```

### Example

```sh
$ ./sync.py /sdcard/DCIM/Camera/ ~/Backups/nick/Camera
```

### One time setup on device
1. [Enable Developer Mode](https://developer.android.com/studio/debug/dev-options#enable)
2. [Enable USB (or Wireless) Debugging](https://developer.android.com/studio/debug/dev-options#Enable-debugging)
3. Accept "Toast" about new host connection.
