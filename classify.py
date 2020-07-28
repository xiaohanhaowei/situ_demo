# -*- encoding: utf-8 -*-
'''
@Author  :   hongwei.wang 
@File    :   classify.py
@Time    :   2020/07/21 10:38:09
@Version :   V1.0
@Contact :   hongwei.wang@lynxi.com
@Desc    :   盗销自行车总队商讨方案
'''

import copy
import json
import os
import random as rd

bike_dict = {
    '盗销自行车_电动车': '101001001',
    '盗销自行车_自行车': '101001002',
    '其他': ''
}


class demo():
    def __init__(self):
        file = open('./library/situ.json', 'rb', encoding='utf-8')
        self.situ_key = json.load(file)
    def run(self):
        pass


def load_rules(path):
    with open(path, 'r', encoding="utf-8") as json_file:
        content = json.load(json_file)

    return content


def check_rules(sentence):
    to_check = sentence.split('；')[-1]
    if len(to_check) <= 20:
        return None
    else:
        return sentence


def single_detect(content, single_slice):
    if single_slice == None:
        return None, None
    else:
        keys = list(content.keys())
        # override the follows to satisfy the TODO-1
        bike_nouns = copy.deepcopy(content[keys[0]]['noun'])
        bike_nouns.extend(content[keys[1]]['noun'])
        # end override
        not_in = 0
        ban_in = False
        # TODO-1  primarily do the elecbike checking then do the bike checking
        correspond_class = None
        prob = 0
        for i in range(2):
            for noun in content[keys[i]]['noun']:
                if noun not in single_slice:
                    not_in += 1
                else:
                    correspond_class = keys[i]
                    break
            if correspond_class is not None:
                break
            # 如果在里边呢？
        if not_in == len(bike_nouns):
            print('不是盗销自行车')
            not_in = 0
            prob = rd.uniform(0.0, 0.1)
            return '其他', prob
        else:
            # 进入下一层: 看是否不符合相关自行车警情
            for ban in sorted(content[correspond_class]['overcome'], key=lambda x: len(x), reverse=True):
                if ban in single_slice:
                    print("ban", ban)
                    ban_in = True
                    break
                else:
                    continue
            if ban_in:
                ban_in = False
                print('不是 %s' % correspond_class)
                prob = rd.uniform(0.2, 0.4)
                return '其他', prob  ## BUG
            # 判断该条是否确切在含有动词，或者词组，如果有就是，没有就是其他。
            verb_grp = content[correspond_class]['verb']
            verb_grp.extend(content[correspond_class]['group'])
            for verb in verb_grp:
                if verb in single_slice:
                    print('in %s' % correspond_class)
                    prob = rd.uniform(0.9, 0.99)
                    return correspond_class, prob
                else:
                    continue
            prob = rd.uniform(0.2, 0.4)
            return '其他', prob


def extract_class(class_name, prob):
    prob = float('%0.4f' % prob) if prob else 0
    if class_name == '其他' or not class_name:
        return {
            'type1': {},
            'type2': {},
            'type3': {}
        }
    else:
        return {
            'type1': {bike_dict[class_name][0:3]: prob},
            'type2': {bike_dict[class_name][0:6]: prob},
            'type3': {bike_dict[class_name]: prob}
        }


path = os.path.join(os.path.dirname(__file__), 'library/new_situ_pos.json')
# path_out = os.path.join(os.path.dirname(__file__), 'library/out_situ_pos.json')
content = load_rules(path)


def update_content(content, online):
    newdict = dict()
    for type1_type2_type3, word_list in online.items():
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
        for type2_type3, word_dict in content.items():
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


def once_forever(sentence, online={}):
    new_content = content
    if online:
        print("start update online data!")
        new_content = update_content(content, online)
    slice_p = check_rules(sentence)
    bike_class, prob = single_detect(new_content, slice_p)
    return extract_class(bike_class, prob)


def single_detect_from_lib(content, single_slice):
    if single_slice == None:
        return None, None
    else:
        keys = list(content.keys())
        # override the follows to satisfy the TODO-1
        bike_nouns = copy.deepcopy(content[keys[0]]['noun'])
        bike_nouns.extend(content[keys[1]]['noun'])
        # end override
        not_in = 0
        ban_in = False
        # TODO-1  primarily do the elecbike checking then do the bike checking
        # for noun in bike_nouns:
        correspond_class = None
        prob = 0
        for i in range(2):
            for noun in content[keys[i]]['noun']:
                if noun not in single_slice:
                    not_in += 1
                    # correspond_class = ''
                else:
                    correspond_class = keys[i]
                    break
            if correspond_class is not None:
                break
            # 如果在里边呢？
        if not_in == len(bike_nouns):
            print('不是盗销自行车')
            not_in = 0
            prob = rd.uniform(0.0, 0.1)
            # return '不是盗销自行车-key'
            return '其他', prob
        else:      
            # for i in range(2):
                # 进入下一层: 看是否不符合相关自行车警情
            for ban in sorted(content[correspond_class]['overcome'], key=lambda x: len(x), reverse=True):
                if ban in single_slice:
                    print(ban)
                    target_ban = ban
                    ban_in = True
                    break
                else:
                    continue
            if ban_in:
                ban_in = False
                print('不是 %s' % correspond_class)
                prob = rd.uniform(0.2,0.4)
                # return '不是盗销自行车-%s' % target_ban
                return '其他'
            # 判断该条是否确切在含有动词，或者词组，如果有就是，没有就是其他。
            verb_grp = content[correspond_class]['verb']
            verb_grp.extend(content[correspond_class]['group'])
            for verb in verb_grp:
                if verb in single_slice:
                    print('in %s' % correspond_class)
                    prob = rd.uniform(0.9, 0.99)
                    return correspond_class, prob
                    
                else:
                    continue
            # return '不是盗销自行车-verbdone'
            prob = rd.uniform(0.2, 0.4)
            return '其他', prob

# 从数据库中推数据
def once_forever_lib(content, single_slice):
    slice_p = check_rules(single_slice)
    bike_class, prob = single_detect(content, slice_p)
    return extract_class(bike_class, prob)

if __name__ == "__main__":
    # slice_p = 'F姜先生报在太玉园小区42号楼2单元，电动自行车被盗。（已复核）7时22分53秒 已复核。(陈迪大)。经民警刘力嘉电话联系，报警人姜国荣（321119196703214370）称2020年7月19日23时许将电动车停放在太玉园东区42号楼2单元单元楼道内，于7时发现电动车不见了，我所民警英明现场开展工作。经请示值班领导赵志明同意上报。'
    # slice_p = '刘占东先生报在潞城镇侉店村60号底商门口，电动车被盗。（已复核）经出现场了解：报警人称其店内工人刘卫峰（男，身份证：412825198111038518，电话：18500279068）2020年7月19日晚22时许将两轮电动车停放在北京市通州区潞城镇侉子店村60号底商海尔电器门店前，7月20日早6时30分许发现其停放的电动车丢失，目前我所主办民警付海涛已受理此事。该警情经主办民警付海涛、值班警长杨超、值班领导袁振龙核实上报。'
    # slice_p = '刘女士报：在西什库大街北大医院第二住院部东门，电动车被盗。（已复核）12时4分6秒 174号已复核。民警徐岩、孙庆晏到现场经了解是报警人早7时将电瓶车停在西什库大街北大医院第二住院部东门，11时发现不见了，民警正在帮其查看监控后受理。反馈民警：王喆 值班领导：阚建良'
    slice_p = '李先生报在北辰西路亚丁湾酒店门口，自行车被盗。（已复核）民警宋旭日现场处置，经核实，报警人于本月17日13时许将自行车（无发票，白色自行车，3成新，价格不详）停放在朝阳区俊峰华亭A座东侧路边后离开，今日回来发现车被盗，周边无监控设备。民警已按行政案件受理。属治安类警情，负责勤务指挥副所长王大未同意上报'
    # slice_p = '李兆龙报：在管庄杨闸地铁（388路）公交站（往北京进京方向），手机被盗。但该群众手机号码机主信息提示黄色警示人员，请予以关注并按相关规范开展工作。（已复核）出警民警刘金文赶赴现场经了解，报警人称停放在管庄乡388路公交车站停放的手机（爱玛牌白色）被盗，现已受理为治安案件，负责勤务指挥领导芦菲同意上报。'
    # slice_p = '报：在望京湖光中街桔子酒店门口，电动车被盗。（已复核）；民警任曲博桑到现场（22时34分）'
    # slice_p = check_rules(slice_p)
    # path = './library/new_situ_pos.json'
    # content = load_rules(path)
    # bike_class, prob = single_detect(content, slice_p)
    # print(extract_class(bike_class, prob))
    # print('bike: {}, prob: {}'.format(bike_dict[bike_class], str(prob)))
    # bike_demo = demo()
    # bike_demo.run()

    online = {
        "公共秩序管理类_盗销自行车_电动车":
            [{"kname":"电动车", "name":"电动摩托车", "type":"noun"},
                {"kname":"被偷", "name":"偷走", "type":"verb"},
                {"kname": "取消报警", "type": "overcome"},
                {"kname": "不属我所管辖", "type": "overcome"}
            ],
        "公共秩序管理类_盗销自行车_自行车":
            [{"kname": "自行车", "name": "脚踏车", "type": "noun"},
                {"kname": "被偷", "name": "偷走", "type": "verb"},
                {"kname": "取消报警", "type": "overcome"},
                {"kname": "不属我所管辖", "type": "overcome"}
            ]
    }
    print("result", once_forever(slice_p, online=online))
