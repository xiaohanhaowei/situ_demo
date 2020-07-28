# -*- coding: utf-8 -*-
import json

from .util import GetValue


# 调用Bert算法函数获取分析数据
def GetDatas(id, info_list, topN, cs):
    ## loadmodel
    # if not cs.loadmodel:
    #     print("First Time Load Model Slowly !")
    #     cs.start()

    # linejson = {"id": id, "sentense": info_list, "topN": topN, "important": important_type}
    linejson = {"id": id, "sentense": info_list, "topN": topN}

    # 输出json
    result = cs.predict_single(linejson)
    # result OrderedDict([('id', 11), ('address', OrderedDict([('13', 0.9103)])), ('type1', {'101': 0.9999}), ('type2', OrderedDict([('101003', 0.9999)])), ('type3', OrderedDict([('101003002', 1.0)])), ('type4', OrderedDict()), ('type5', OrderedDict())])

    return result


# 保存json文件
def SaveJsonFile(filename, types):
    with open(filename, 'w') as file_obj:
        json.dump(types, file_obj)


# 加载json文件数据
def LoadJsonFile(filename):
    with open(filename) as file_obj:
        types = json.load(file_obj)
    return types


# 处理模型
def DecryptModel(filename, value):
    with open(filename, "rb+") as f:
        for i in range(5):
            data = f.read(value)
            data = data[::-1]
            f.seek(-value, 1)
            f.write(data)


# 初始化
def Init(modelFile):
    value = int(GetValue())
    DecryptModel(modelFile, value)
