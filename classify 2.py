# -*- encoding: utf-8 -*-
'''
@Author  :   hongwei.wang 
@File    :   classify.py
@Time    :   2020/07/21 10:38:09
@Version :   V1.0
@Contact :   hongwei.wang@lynxi.com
@Desc    :   盗销自行车总队商讨方案
'''

import json
class demo():
    def __init__(self):
        file = open('./library/situ.json', 'rb')
        self.situ_key = json.load(file, encoding='utf-8')
        # data = json_loader.read().decode(encoding='gbk').encode(encoding='utf-8')
        # self.situ_content = js.dumps(js.loads(data), ensure_ascii=False)
        
    def run(self):
        pass


def load_rules(path):
    json_file = open(path, 'rb')
    content = json.load(json_file, encoding='utf-8')
    # content = json.dumps(content, ensure_ascii=False)
    return content


def single_detect(content, single_slice):
    keys = list(content.keys())
    # keys = [i.encode('utf-8') for i in keys]
    bike_nouns = content[keys[0]]['noun']
    bike_nouns.extend(content[keys[1]]['noun'])
    not_in = 0
    ban_in = False

    for noun in bike_nouns:
        if noun not in single_slice:
            not_in += 1
        else:
            break
        # 如果在里边呢？

    if not_in == len(bike_nouns):
        print('不是盗销自行车')
        not_in = 0
        return  
    else:      
        for i in range(2):
            # 进入下一层: 看是否不符合相关自行车警情
            for ban in content[keys[i]]['overcome']:
                if ban in single_slice:
                    ban_in = True
                    break
                else:
                    continue
            if ban_in == True:
                ban_in = False
                print('不是 %s' % keys[i])
                continue
            # 判断该条是否确切在含有动词，或者词组，如果有就是，没有就是其他。
            verb_grp = content[keys[i]]['verb']
            verb_grp.extend(content[keys[i]]['group'])
            for verb in verb_grp:
                if verb in single_slice:
                    print('in %s' % keys[i])
                else:
                    print('not in %s-verb&verbgroup' % keys[i])
        
    

if __name__ == "__main__":
    slice_p = '李女士报在阜外医院东门对面公交车站，自行车被盗；找到了又'
    path = './library/new_situ_pos.json'
    content = load_rules(path)
    single_detect(content, slice_p)
    # bike_demo = demo()
    # bike_demo.run()

