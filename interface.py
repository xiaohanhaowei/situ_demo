# -*- encoding: utf-8 -*-
'''
@Author  :   hongwei.wang 
@File    :   interface.py
@Time    :   2020/07/29 10:09:58
@Version :   V1.0
@Contact :   hongwei.wang@lynxi.com
@Desc    :   None
'''


class api_interface():
    
    def __init__(self, content):
        self.content = content


    def update_content(self, online):
        '''
        @Author: hongwei.wang
        @date: 2020-07-29
        @func: 
        @args: 
            content: json instance that need update
            online: the manually updated content that need to update to the json instance
            operation: string type, either 'del' or 'add'
        @return: 
        @raise: 
        '''
        newdict = dict()
        for type1_type2_type3, word_list, operation in online.items():
            if "_" not in type1_type2_type3:
                print("The type label is not right : 'type1_type2_type3'")
                continue
            type2_3 = "_".join(type1_type2_type3.split("_")[1:3])
            
            subdict = dict()
            for wd in word_list:
                keyword = wd.get("kname", "")
                simword = wd.get("name", "")
                type_ = wd.get("type", "")
                if keyword not in subdict:
                    subdict[keyword] = list()
                    subdict[keyword].append(keyword)
                    if simword:
                        subdict[keyword].append(simword)
                else:
                    if simword:
                        subdict[keyword].append(simword)
                if type_ not in subdict:
                    subdict[type_] = list()
                    subdict[type_].append(keyword)
                else:
                    subdict[type_].append(keyword)
            newdict[type2_3] = subdict

        if newdict:
            new_content = dict()
            for type2_type3, word_dict in self.content.items():
                sudict = newdict.get(type2_type3, {})
                if subdict:
                    for i, k in enumerate(["verb", "noun", "space", "group", "overcome"]):
                        words = word_dict.get(k, [])
                        new_words = sudict.get(k, [])
                        inter_words = list(set(words).intersection(set(new_words))) if k != "overcome" else new_words

                        for w in inter_words:
                            simwords = subdict.get(w, [])
                            words.extend(simwords)
                        words = list(set(words))
                        word_dict[k] = words
                        new_content[type2_type3] = word_dict
                else:
                    new_content[type2_type3] = word_dict
            # with open(path_out, 'w', encoding="utf-8") as json_out:
            with open(path, 'w', encoding="utf-8") as json_out:
                json.dump(new_content, json_out, ensure_ascii=False, indent=2)
            if new_content:
                return new_content
            else:
                return content
        else:
            return content