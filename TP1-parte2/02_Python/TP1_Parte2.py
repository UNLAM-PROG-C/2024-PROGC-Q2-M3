import threading
import sys
import math
import os
import time
import re
PATH = os.path
mtx_count = threading.Lock()
count_char = 0

def read_line(lines:list[str], start ,end ):
    global count_char
    for i in range(start, end):
        with mtx_count:
            count_char += len(re.sub(r'[^a-zA-Z0-9]', '', lines[i]).strip().replace('\n',''))

def read_file(path:str, n_thread:int ):
    start_time = time.time()
    threads: list[threading.Thread] = []
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            num_lines = len(lines)
            chunk_size = math.ceil(num_lines / n_thread)
            for i in range(n_thread):
                start = i * chunk_size
                end = min(start + chunk_size, num_lines)
                thd = threading.Thread(target=read_line, args=(lines, start ,end))
                thd.start()
                threads.append(thd)
            for thd in threads:
                thd.join()
        end_time = time.time()
        print(f"Caracteres contados con {n_thread} thread/s: {count_char}")
        print(f"Tiempo con {n_thread} thread/s: { (end_time-start_time)* 1000}")
    except FileNotFoundError:
        print(f"File not found at path '{path}'.")
    except IOError as e:
        print(f"Error reading file: {e}")

def read_param() -> tuple[str, int]:
    if len(sys.argv) != 3:
        print(f'Use: python {sys.argv[0]}.py <path_al_archivo> <num_thread>')
        sys.exit(1)
    else:
        try:
            thread = int(sys.argv[2])
        except ValueError as e:
            print(e)
            sys.exit(1)
        return sys.argv[1],thread

def main():
    path,thread = read_param()
    read_file(path,thread)

if __name__ == '__main__':
    main()