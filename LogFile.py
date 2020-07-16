
def logging_dict(path):
    _name_log = path+"\\log_file.log"
    print("  Где лежит лог файл", _name_log)

    dictLogConfig = {
        "version":1,
        "handlers":{

            "fileHandler":{
                "class":"logging.FileHandler",
                "formatter":"myFormatter",
                "filename":_name_log
            }
        },
        "loggers":{
            "exampleApp":{
                "handlers":["fileHandler"],
                "level":"INFO",
            }
        },
        "formatters":{
            "myFormatter":{
                "format":"%(asctime)s - %(levelname)s - %(message)s"
            }
        }
    }
    return  dictLogConfig
