import os
import sys
import time


def main():
    print(f"PID: {os.getpid()} PPID: {os.getppid()} Letra: A")
    time.sleep(5)

    pid = os.fork()

    if pid < 0:
        sys.exit("Error al crear el primer proceso.")

    if pid == 0: # A crea B
        print(f"PID: {os.getpid()} PPID: {os.getppid()} Letra: B")
        time.sleep(5)

        pid = os.fork()
        if pid == 0: # B crea C
            print(f"PID: {os.getpid()} PPID: {os.getppid()} Letra: C")
            time.sleep(5)

            pid = os.fork()
            if pid == 0: # C crea E
                print(f"PID: {os.getpid()} PPID: {os.getppid()} Letra: E")
                time.sleep(5)

                pid = os.fork()
                if pid == 0: # E crea H
                    print(f"PID: {os.getpid()} PPID: {os.getppid()} Letra: H")
                    time.sleep(5)
                else:
                    pid = os.fork()
                    if pid == 0: # E crea I
                        print(f"PID: {os.getpid()} PPID: {os.getppid()} Letra: I")
                        time.sleep(5)
        else: # B crea D
            pid = os.fork()
            if pid == 0:
                print(f"PID: {os.getpid()} PPID: {os.getppid()} Letra: D")
                time.sleep(5)

                pid = os.fork()
                if pid == 0: # D crea F
                    print(f"PID: {os.getpid()} PPID: {os.getppid()} Letra: F")
                    time.sleep(5)
                else:
                    pid = os.fork()
                    if pid == 0: # D crea G
                        print(f"PID: {os.getpid()} PPID: {os.getppid()} Letra: G")
                        time.sleep(5)
    
    while True:
        try:
            os.wait()
        except ChildProcessError:
            break


if __name__ == "__main__":
    main()
