import argparse
import subprocess

from adapt import default_encoding
default_encoding()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler operation.", add_help=False)
    parser.add_argument("--token", action="store_true", help="create DS token")
    parser.add_argument("--project", action="store_true", help="DS project operation")
    parser.add_argument("--tenant", action="store_true", help="DS tenant operation")
    parser.add_argument("--queue", action="store_true", help="DS queue operation")
    parser.add_argument("--resource", action="store_true", help="DS resource operation")
    parser.add_argument("--process", action="store_true", help="DS process definition operation")
    parser.add_argument("--scheduler", action="store_true", help="DS scheduler operation")
    parser.add_argument("--run", action="store_true", help="DS complement data operation")
    parser.add_argument("--instance", action="store_true", help="DS instance operation")
    args, unknown = parser.parse_known_args()

    if args.token:
        subprocess.run(["python", "handle/token_handle.py"] + unknown)
    elif args.project:
        subprocess.run(["python", "handle/project_handle.py"] + unknown)
    elif args.tenant:
        subprocess.run(["python", "handle/tenant_handle.py"] + unknown)
    elif args.queue:
        subprocess.run(["python", "handle/queue_handle.py"] + unknown)
    elif args.resource:
        subprocess.run(["python", "handle/resource_handle.py"] + unknown)
    elif args.process:
        subprocess.run(["python", "handle/process_handle.py"] + unknown)
    elif args.run:
        subprocess.run(["python", "handle/run_handle.py"] + unknown)
    elif args.instance:
        subprocess.run(["python", "handle/instance_handle.py"] + unknown)
    elif args.scheduler:
        subprocess.run(["python", "handle/scheduler_handle.py"] + unknown)
    else:
        parser.print_help()

