# -*- encoding: utf-8 -*-
'''
@Author  :   hongwei.wang 
@File    :   interface.py
@Time    :   2020/07/29 10:09:58
@Version :   V1.0
@Contact :   hongwei.wang@lynxi.com
@Desc    :   None
'''

import json
import os


class api_interface():

    def __init__(self):
        self.jsonpath = os.path.join(os.path.dirname(__file__), 'library/new_situ_pos.json')
        self.content = {}
        self.load_json()

    def load_json(self):
        with open(self.jsonpath, 'r', encoding="utf-8") as json_file:
            self.content = json.load(json_file)

    # 根据label 获取对应字典
    def from_label_get_dict(self, type1_type2_=""):
        if "_" not in type1_type2_:
            print("%s not in situ library, can not pull" % type1_type2_)
            return {}
        else:
            type2_ = "_".join(type1_type2_.split("_")[1:])
            subdict = self.content.get(type2_, {})
            get_dict = dict([(k, subdict.get(k, [])) for k in ["verb", "noun", "overcome"]])
            return get_dict

    # 根据online 数据 增删本地json数据
    def update_content(self, type1_type2_="", wordlist=[], sign=""):
        if "_" in type1_type2_:
            type2_ = "_".join(type1_type2_.split("_")[1:])
            subdict = self.content.get(type2_, {})
            for w, worddict in enumerate(wordlist):
                word = worddict.get("kname", "")
                type_ = worddict.get("type", "")
                if type_ not in subdict:
                    if type_:
                        subdict[type_] = list()
                        subdict[type_].append(word)
                    else:
                        print("%s not in situ library, can not update content" % type_)
                else:
                    words = subdict[type_]
                    if sign == "add" and word:
                        words.append(word)
                    elif sign == "del" and word in words and type_ == "overcome":
                        words.remove(word)
                    subdict[type_] = list(set(words))
                    self.content[type2_] = subdict
            with open(self.jsonpath, 'w', encoding="utf-8") as json_out:
                json.dump(self.content, json_out, ensure_ascii=False, indent=2)
        else:
            print("%s not in situ library, can not update content" % type1_type2_)


if __name__ == "__main__":
        infer = api_interface()
        print("infer.content", infer.content)

        print("from_label_get_dict", infer.from_label_get_dict("公共秩序管理类_盗销自行车_电动车"))

        infer.update_content(
            type1_type2_="公共秩序管理类_盗销自行车_电动车",
            wordlist=[{"kname": "取消报警####", "type": "overcome"}],
            sign="add")

        infer.update_content(
            type1_type2_="公共秩序管理类_盗销自行车_电动车",
            wordlist=[{"kname": "山地车####", "type": "noun"}],
            sign="add")

        # infer.update_content(
        #     type1_type2_="公共秩序管理类_盗销自行车_电动车",
        #     wordlist=[{"kname": "取消报警####", "type": "overcome"}],
        #     sign="del")
        #
        # infer.update_content(
        #     type1_type2_="公共秩序管理类_盗销自行车_电动车",
        #     wordlist=[{"kname": "山地车####", "type": "noun"}],
        #     sign="del")
