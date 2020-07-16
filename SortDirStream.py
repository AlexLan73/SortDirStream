import sys, os, glob
import logging.config

import threading
import threading as Thread
import time


from LogFile import *

logger = {}

# pyinstaller -F SortDirStream.py

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
    if is_prog:
        is_prog = False
        x = threading.Thread(target=read_dir_files, daemon=True)
        x.start()

class MyThread(threading.Thread):
    def __init__(self, event, fun):
        threading.Thread.__init__(self)
        self.stopped = event
        self.fun = fun

    def run(self):
        while not self.stopped.wait(0.1):
            self.fun()

def parse_input_arguments():
    name_file_run = __file__
    ls_arg = sys.argv
    k = 0
    for it in ls_arg:
        _s = " Номер аргумента -{} значение ->  {} ".format(k, it)
        print(_s)
        logger.info(_s)
        k += 1

    if len(ls_arg) < 1:
        print(" нет файла в аргументах")
        logger.critical(" нет файла в аргументах")
        sys.exit(-1)

    if os.path.isdir(ls_arg[1]):
        logger.info(" - обработка dir {}".format(ls_arg[1]))
        return [ls_arg[0], ls_arg[1]]

    print("Проблема с аргументами {} - нет каталога ".format(ls_arg[1]))
    logger.critical("Проблема с аргументами {} - нет каталога   <- !!! ".format(ls_arg[1]))
    sys.exit(-1)


if __name__ == "__main__":
    print(" == START ==")
    path ="E:\\1\\CSM UniCAN2\\UNICAN CONVERTED FILES"

    _path_log = "C:\\CSM UniCAN2\\UNICAN CONVERTED FILES\\"
    dictLogConfig = logging_dict(_path_log)
    logging.config.dictConfig(dictLogConfig)
    logger = logging.getLogger("exampleApp")
    logger.info("START")

    __path_start = parse_input_arguments()

    stopFlag = threading.Event()
    thread = MyThread(stopFlag, Start_module)

    thread.start()

    time.sleep(5)
    stopFlag.set()
    while not (is_prog):
        print(is_prog, "-----  !!!!!!!!!!!! while ")
        time.sleep(0.3)
        pass
