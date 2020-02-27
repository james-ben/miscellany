import sys
import time
import argparse
import subprocess as sp
try:
    import psutil
except ImportError:
    print("This script requires the package `psutil` to run.",
            file=sys.stderr)
    print("Please install with `python3 -m pip install psutil`",
            file=sys.stderr)
    sys.exit(1)

# TODO: refactor to use a class


class ProcessGone(Exception):
    pass


def findProcByName(name, script=None):
    procs = []
    for p in psutil.process_iter(attrs=['name', 'cmdline']):
        if p.info['name'] == name:
            cmdl = ' '.join(p.cmdline())
            # filter more by string in command line invocation
            if (script is not None) and (script in cmdl):
                procs.append(p)
            else:
                procs.append(p)
    if not procs:
        raise ProcessGone("Could not find any processes")
    return procs


def getMemUsage(proc):
    p0 = sp.Popen(['pmap', str(proc.pid)], stdout=sp.PIPE)
    print(proc.info['name'], end=': ')
    print(p0.stdout.readlines()[-1].decode().split()[1])


def doStuff(pName, cmdline):
    procs = findProcByName(pName, cmdline)
    for p in procs:
        # print(p)
        getMemUsage(p)


def parseArgs():
    parser = argparse.ArgumentParser(description="Track the memory usage of a process.")
    parser.add_argument('-n', '--name', type=str,
                        help="Name to search for.")
    parser.add_argument('-c', '--cmdline', type=str, 
                        help="Filter by another string on the command line.")
    # TODO: search by process ID
    args = parser.parse_args()
    return args


def main():
    args = parseArgs()
    pName = args.name
    if args.cmdline:
        cmdline = args.cmdline
    else:
        cmdline = None

    while True:
        try:
            doStuff(pName, cmdline)
        except ProcessGone:
            print("Process has disappeared, exiting", file=sys.stderr)
            break
        time.sleep(10)


if __name__ == '__main__':
    main()
