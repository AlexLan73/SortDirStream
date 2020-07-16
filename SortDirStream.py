import threading
import threading as Thread
import time

is_prog = True

def read_dir_files():
    global is_prog
    is_prog = False
    print(" --- start  -- ")
    for i in range(15):
        print(i, time.ctime())
        time.sleep(0.1)
    print("--- end  --  ")
    is_prog = True


def Start_module():
    global is_prog
#    print(is_prog, " --  ",time.ctime())
    if is_prog:
        is_prog = False
        print( "  !!!!!!!!!!!! foo1 ")
#        x = threading.Thread(target=read_dir_files, args=(1,), daemon=True)
        x = threading.Thread(target=read_dir_files,  daemon=True)
        x.start()


class MyThread(threading.Thread):
    def __init__(self, event, fun):
        threading.Thread.__init__(self)
        self.stopped = event
        self.fun = fun

    def run(self):
        while not self.stopped.wait(0.1):
            self.fun()

if __name__ == "__main__":
    print(" == START ==")
    stopFlag = threading.Event()
    thread = MyThread(stopFlag, Start_module)
    thread.start()
    # this will stop the timer
    time.sleep(5)
    stopFlag.set()
    while not(is_prog):
        print(is_prog, "-----  !!!!!!!!!!!! while ")
        time.sleep(0.3)
        pass

