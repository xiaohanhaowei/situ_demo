# -*- coding:utf-8 -*-
import logging.config

import yaml


# 加载配置文件
def LoadLogging(configPath):
    if configPath == "":
        configPath = './log_cfg.yml'
    with open(configPath) as log_cfg_file:
        log_dictcfg = yaml.safe_load(log_cfg_file)
    logging.config.dictConfig(log_dictcfg)

    logger = logging.getLogger('file')
    return logger
