import sys, os, glob, time
import logging.config
import threading
from LogFile import *

logger, path_file_logger, is_prog, path_dan = {}, "", True, ""


# pyinstaller -F SortDirStream.py


def direct(path_dir):
    global logger
    if not (os.path.isdir(path_dir)):
        os.mkdir(path_dir)
        if os.path.isdir(path_dir):
            logger.info(" dir -> {}".format(path_dir))
        else:
            logger.warning(" dir -> {}".format(path_dir))


def read_dir_files():
    global is_prog, path_dan, logger, path_file_logger

    def _test_log_file():
        _files = glob.glob(path_dan)
        _f = [x for x in _files if not ((".log" in x.lower()) or ("~" in x.lower()))]
        _count = len(_f)
        return (_count, _f)

    is_prog = False
    _count_files = len(glob.glob(path_dan))
    _fils_dan = _test_log_file()
    _count_files = _fils_dan[0]
    while _count_files > 0:
        _fils_dan = _test_log_file()
        _files = _fils_dan[1]
        for _file in _files:
            _name_file_basa = os.path.basename(_file)
            path_dir = os.path.dirname(_file)

            __i = _name_file_basa.rindex(".")
            _name_file0 = _name_file_basa[:__i]
            # разбор названия
            p = ["", "", ""]
            __i = _name_file0.rindex("_")
            p[1] = _name_file0[__i + 1:]
            _name_file1 = _name_file0[:__i - 16]
            __i = _name_file1.rindex("-")
            p[2] = _name_file1[__i + 1:].split("_")[0]
            p[0] = _name_file1[:__i]

            direct(path_dir)
            path_dir = path_dir + "\\" + p[0]
            direct(path_dir)
            path_dir = path_dir + "\\" + p[2]
            direct(path_dir)
            path_dir = path_dir + "\\" + p[1]
            direct(path_dir)
            __path = path_dir + "\\" + _name_file_basa
#            logger.info(" - перемещаем файл {}".format(__path))
            if os.path.isfile(__path):
                os.remove(__path)
            try:
                with open(_file) as f:
                    pass
                os.rename(_file, __path)

            except:
                logger.warning(" - файл {}  занят другой программой ".format(__path))

            if os.path.isfile(__path):
                logger.info(" -  файл {}  перемещен".format(__path))
            else:
                logger.warning(" - проблема с перемещением файл {}".format(__path))

            statinfo = os.stat(path_file_logger)
            if statinfo.st_size >= 104857600:  # if statinfo.st_size >= 1024*10:
                inicial_logging()

        _fils_dan = _test_log_file()
        _count_files = _fils_dan[0]
    is_prog = True


def Start_module():
    global is_prog, logger
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
        while not self.stopped.wait(1):
            self.fun()


def parse_input_arguments():
    name_file_run = __file__  # путь старта программы
    _dargs = dict(
        s_error="Ok!",
        kod_error=0,
        dir_start="",
        dir_work="",
        ls_arg=[]
    )

    ls_arg = sys.argv
    k = 0

    for it in ls_arg:
        _s = " Номер аргумента -{} значение ->  {} ".format(k, it)
        print(_s)
        _dargs["ls_arg"] += [_s]
        k += 1

    if len(ls_arg) < 2:
        _dargs["kod_error"] = -1
        _dargs["s_error"] = " нет  аргументов  код -1"
        print(_dargs["s_error"])
        return _dargs

    _dargs["dir_start"] = os.path.dirname(ls_arg[0])
    if not (os.path.isdir(_dargs["dir_start"])):
        _dargs["kod_error"] = -2
        _dargs["s_error"] = "Не правильно определился каталог старта програмы  код -2"
        return _dargs

    _dargs["dir_work"] = ls_arg[1]
    if not (os.path.isdir(_dargs["dir_work"])):
        _dargs["kod_error"] = -3
        _dargs["s_error"] = "Нет директории с данными код -3"
        return _dargs

    return _dargs


def inicial_logging():
    global logger, path_file_logger
    _path_log = path_file_logger + "\\LOG"

    if not (os.path.isdir(_path_log)):
        os.mkdir(_path_log)

    dictLogConfig = logging_dict(_path_log)
    path_file_logger = dictLogConfig['handlers']["fileHandler"]["filename"]

    logging.config.dictConfig(dictLogConfig)
    logger = logging.getLogger("exampleApp")
    logger.info("START")

def fprint(x):
    for it in x: print(it)

def error_args(_args):
    global logger, path_file_logger
    if _args["kod_error"] != 0:
        # проблема с конфигурацией
        if _args["kod_error"] ==-1:
            print(_args["s_error"] )
            fprint(_args["ls_arg"])
            sys.exit(_args["kod_error"])

        elif _args["kod_error"] ==-2:
            print(_args["s_error"] )
            fprint(_args["ls_arg"])
            sys.exit(_args["kod_error"])

        elif _args["kod_error"] ==-3:
            print(_args["s_error"] )
            fprint(_args["ls_arg"])
            path_file_logger = _args["dir_start"]
            inicial_logging()
            for it in _args["ls_arg"]:
                logger.info(it)
            logger.critical(_args["s_error"])
            sys.exit(_args["kod_error"])


if __name__ == "__main__":
    print(" == START ==")
    __arguments = parse_input_arguments()

    if __arguments["kod_error"] != 0:
        # проблема с аргументами
        error_args(__arguments)

    print(__arguments["s_error"] )
    fprint(__arguments["ls_arg"])
    path_file_logger = __arguments["dir_start"]
    inicial_logging()
    for it in __arguments["ls_arg"]:
        logger.info(it)

    path_dan = __arguments["dir_work"] + "\\*.*"

    stopFlag = threading.Event()
    thread = MyThread(stopFlag, Start_module)

    thread.start()

    while True:
        time.sleep(60)

    stopFlag.set()

    logger.info("END нормальное завершение программы")
