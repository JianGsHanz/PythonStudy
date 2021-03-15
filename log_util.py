# coding=utf-8
import logging

def log(msg):
    # 创建logger，如果参数为空则返回root logger
    logger = logging.getLogger("mylogger")
    logger.setLevel(logging.DEBUG)  # 设置logger日志等级

    if not logger.handlers:
        # 创建handler
        fh = logging.FileHandler("test.log", encoding="utf-8")
        ch = logging.StreamHandler()

        # 设置输出日志格式
        formatter = logging.Formatter(
            fmt="%(asctime)s %(name)s %(filename)s %(message)s",
            datefmt="%Y/%m/%d %X"
        )

        # 为handler指定输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 为logger添加的日志处理器
        logger.addHandler(fh)
        logger.addHandler(ch)

    # 输出不同级别的log
    logger.info(msg)
