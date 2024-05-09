import argparse
import subprocess

from adapt import default_encoding
default_encoding()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler operation.", add_help=False)
    parser.add_argument("--token", action="store_true", help="create DS token")
    parser.add_argument("--tenant", action="store_true", help="DS tenant operation")
    args, unknown = parser.parse_known_args()

    if args.token:
        subprocess.run(["python", "handle/token_handle.py"] + unknown)
    elif args.tenant:
        subprocess.run(["python", "handle/tenant_handle.py"] + unknown)
    else:
        parser.print_help()

