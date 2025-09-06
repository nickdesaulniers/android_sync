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