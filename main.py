import argparse
import subprocess

from adapt import default_encoding
default_encoding()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler operation.", add_help=False)
    parser.add_argument("--token", action="store_true", help="create DS token")
    args, unknown = parser.parse_known_args()

    if args.token:
        subprocess.run(["python", "request/create_token.py"] + unknown)
    else:
        parser.print_help()

