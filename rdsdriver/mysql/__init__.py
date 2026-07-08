# -*- coding: utf-8 -*-
import importlib
import logging
import sys
from .driver import *
from .cursors import *


logger = logging.getLogger(__name__)


def WrapAttrs(source_module_name, target_module_name):
    source_module = importlib.import_module(source_module_name)
    target_module = sys.modules[target_module_name]
    if hasattr(source_module, "__all__"):
        attrs = source_module.__all__
    else:
        # 没有定义__all__，则获取所有不以下划线开头的属性
        attrs = [attr for attr in dir(source_module) if not attr.startswith("_")]
    attrs.append("DATETIME")
    attrs.append("ROWID")

    # 遍历__all__中的每个属性名
    for attr in attrs:
        # 检查该属性是否已经在当前模块中存在
        if not hasattr(target_module, attr):
            # 从源模块获取属性值
            attr_value = getattr(source_module, attr)
            # 将属性动态设置到当前模块中
            setattr(target_module, attr, attr_value)
            logger.debug(f"已添加属性: {attr}")
        else:
            logger.debug(f"跳过已存在属性: {attr}")


WrapAttrs("pymysql", __name__)
