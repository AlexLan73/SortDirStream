import sys, os, glob
import logging.config

import threading
import threading as Thread
import time


from LogFile import *

logger = {}

# pyinstaller -F SortDirStream.py

is_prog = True
path_dan =""

def direct(path_dir):
    if not(os.path.isdir(path_dir)):
        logger.info(" создает dir - {}".format(path_dir))
        os.mkdir(path_dir)
        if os.path.isdir(path_dir):
            pass
            logger.info(" dir - {}   # создана".format(path_dir))
        else:
            pass
            logger.warning(" dir - {}   # проблема создания ".format(path_dir))


def read_dir_files():
    global is_prog, path_dan, logger
    is_prog = False
#    print(" --- start  -- ")
    _count_files = len(glob.glob(path_dan))

    while _count_files>0:
         _files = glob.glob(path_dan)
         for _file in _files:
            _name_file_basa =os.path.basename(_file)
            path_dir =os.path.dirname(_file)

            __i  = _name_file_basa.rindex(".")
            _name_file0 = _name_file_basa[:__i]

            p=["","",""]
            __i = _name_file0.rindex("_")
            p[1] =  _name_file0[__i+1:]
            _name_file1 = _name_file0[:__i-16]
            __i = _name_file1.rindex("-")
            p[2] = _name_file1 [__i+1:].split("_")[0]
            p[0] = _name_file1[:__i]

            direct(path_dir)
            path_dir = path_dir + "\\" + p[0]
            direct(path_dir)
            path_dir = path_dir + "\\" + p[2]
            direct(path_dir)
            path_dir = path_dir + "\\" + p[1]
            direct(path_dir)
            __path = path_dir+"\\"+_name_file_basa
            logger.info(" - перемещаем файл {}".format(__path))
            if os.path.isfile(__path):
                os.remove(__path)
            os.rename(_file, __path)

            if os.path.isfile(__path):
                 logger.info(" -  файл {}  перемещен".format(__path))
            else:
                 logger.warning(" - проблема с перемещением файл {}".format(__path))
         _count_files = len(glob.glob(path_dan))
#    print("--- end  --  ")
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
        while not self.stopped.wait(0.5):
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
#    path_dan ="E:\\1\\CSM UniCAN2\\UNICAN CONVERTED FILES\\*.*"
    _path_log = "C:\\CSM UniCAN2\\UNICAN CONVERTED FILES"

    dictLogConfig = logging_dict(_path_log)
    logging.config.dictConfig(dictLogConfig)
    logger = logging.getLogger("exampleApp")
    logger.info("START")

    __path_start = parse_input_arguments()
    path_dan = __path_start[1]+"\\*.*"

    stopFlag = threading.Event()
    thread = MyThread(stopFlag, Start_module)

    thread.start()

    while True:
        time.sleep(60)

    stopFlag.set()

    logger.info("END нормальное завершение программы")
