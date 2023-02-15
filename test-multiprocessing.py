import multiprocessing
import time


def func1():
    while True:
        print("func 1")
        time.sleep(1)

def func2():
    while True:
        print("func 2")
        time.sleep(1)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=func1)
    p2 = multiprocessing.Process(target=func2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

#p2 = multiprocessing.Process(target=func2)