import sys
import commands

def main():
    if len(sys.argv) < 3 or sys.argv[2] not in commands.__all__:
        print(f"Usage: {', '.join(commands.__all__) }")
        return

    command = sys.argv[2]
    args = sys.argv[3:]
    try:
        cmd=getattr(commands,command)
        cmd(*args)
    except ImportError:
        print(f"Error: Command '{command}' is not supported.")
        return


if __name__ == '__main__':
    main()
