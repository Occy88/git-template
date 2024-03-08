import sys
from . import commands
def main():
    if len(sys.argv) < 2 or sys.argv[1] not in commands.__all__:
        print(f"Usage: {', '.join(commands.__all__) }")
        return

    command = sys.argv[1]
    args = sys.argv[2:]
    try:
        cmd=getattr(commands,command)
        cmd(*args)
    except ImportError:
        print(f"Error: Command '{command}' is not supported.")
        return


if __name__ == '__main__':
    main()
