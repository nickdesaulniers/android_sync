#!/usr/bin/env python

import sys
import time
from argparse import ArgumentParser
from pathlib import Path
from subprocess import PIPE, Popen


def get_remote_files(source: Path) -> list[Path]:
    command = f"adb shell find {source}"
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        err = stderr.decode().strip()
        print(f"Error getting remote files: {err}", file=sys.stderr)
        if "adb: no devices/emulators found" in err:
            print("Make sure your Android device is connected and ADB is set up correctly.", file=sys.stderr)
            print("Enable developer options by tapping on", file=sys.stderr)
            print("Settings > About phone > Build number", file=sys.stderr)
            print("seven times. Then enable USB debugging in Settings > Developer options.", file=sys.stderr)
        sys.exit(1)
    return [Path(line) for line in stdout.decode().splitlines()][1:]


def get_local_files(destination: Path) -> list[Path]:
    if not destination.exists():
        print(f"Destination file or directory does not exist: {destination}", file=sys.stderr)
        sys.exit(1)
    if not destination.is_dir():
        print(f"Destination is not a directory: {destination}", file=sys.stderr)
        sys.exit(1)
    return [Path(line) for line in destination.glob("**/*") if line.is_file()]


def get_files_to_sync(remote_files: list[Path], local_files: list[Path]) -> list[Path]:
    remote_set = set([path.name for path in remote_files])
    local_set = set([path.name for path in local_files])
    return list(remote_set - local_set)


def adb_pull_one(remote_path: Path, local_path: Path, verbose: bool) -> bool:
    local_path.parent.mkdir(parents=True, exist_ok=True)
    if verbose:
        print(f"Pulling {remote_path} to {local_path}")
    command = f"adb pull -z zstd {remote_path} {local_path}"
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    _, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error pulling file {remote_path}: {stderr.decode()}", file=sys.stderr)
        return False
    if verbose:
        print(f"Pulled {remote_path} to {local_path}")
    return True


def adb_pull_all(destination: Path, files_to_sync: list[Path], remote_base: Path, verbose: bool):
    print(f"Starting to pull {len(files_to_sync)} file(s)...")
    start_time = time.time()
    failures = 0

    for file in files_to_sync:
        remote_path = remote_base / file
        local_path = destination / file
        if not adb_pull_one(remote_path, local_path, verbose):
            failures += 1

    print(f"Pulled {len(files_to_sync) - failures} file(s) successfully in {time.time() - start_time:.2f} seconds.")
    if failures > 0:
        print(f"Failed to pull {failures} file(s).", file=sys.stderr)


def main():
    parser = ArgumentParser(description="Sync files from Android device")
    parser.add_argument("source", type=Path, help="Source file or directory on Android device")
    parser.add_argument(
        "destination", type=Path, help="Destination directory on local machine"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    print(f"Syncing {args.source} to {args.destination}.")
    print("Searching for files on remote device...")
    remote_files = get_remote_files(args.source)
    print(f"{len(remote_files)} file(s) found on remote device.")
    local_files = get_local_files(args.destination)
    print(f"{len(local_files)} file(s) found locally.")
    files_to_sync = get_files_to_sync(remote_files, local_files)
    print(f"{len(files_to_sync)} file(s) to sync.")
    if files_to_sync:
        adb_pull_all(args.destination, files_to_sync, remote_files[0].parent, args.verbose)

if __name__ == "__main__":
    main()
