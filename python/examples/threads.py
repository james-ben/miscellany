import time
import shlex
import threading
import subprocess as sp


def thread_printer(flag):
    counter = 0
    while not flag():
        print("hello " + str(counter))
        counter += 1
        time.sleep(1)


def complex_thread(flag, handle):
    counter = 0
    while not flag():
        for line in iter(handle.stdout.readline, b''):
            if flag():
                break
            if handle.poll() is not None:
                time.sleep(0.1)
            print("hello {} ({})".format(counter, len(line)))
            counter += 1
            time.sleep(1)


def reading_thread(flag, handle):
    while not flag():
        for line in iter(handle.stdout.readline, b''):
            if flag():
                break
            print(line.decode().rstrip())


def main():
    # demonstrate killing threads with a flag
    myFlag = False
    t1 = threading.Thread(target=thread_printer, args=(lambda: myFlag, ))
    t1.start()

    # demonstrate more complicated thread which reads from a subprocess
    handle = sp.Popen(['cat', '/dev/urandom'], stdout=sp.PIPE, stderr=sp.STDOUT)
    t2 = threading.Thread(target=complex_thread, args=(lambda: myFlag, handle))
    t2.start()

    # demonstrate problem where it can block indefinitely waiting for the next
    #  bit of input from the subprocess output stream
    cmdStr2 = "sleep 3 && echo \"hi\" && sleep 4 && echo \"there\""
    handle2 = sp.Popen(cmdStr2, stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
    t3 = threading.Thread(target=reading_thread, args=(lambda: myFlag, handle2))
    t3.start()

    time.sleep(5)
    myFlag = True
    t1.join()
    t2.join()
    t3.join()
    print("Completed execution")


if __name__ == '__main__':
    main()
