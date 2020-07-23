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
        return '不是盗销自行车-key'
    else:      
        for i in range(2):
            # 进入下一层: 看是否不符合相关自行车警情
            for ban in content[keys[i]]['overcome']:
                if ban in single_slice:
                    print(ban)
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
                    return keys[i]
                else:
                    print('not in %s-verb&verbgroup' % keys[i])
        return '不是盗销自行车'
    

if __name__ == "__main__":
    # slice_p = 'F姜先生报在太玉园小区42号楼2单元，电动自行车被盗。（已复核）7时22分53秒 已复核。(陈迪大)。经民警刘力嘉电话联系，报警人姜国荣（321119196703214370）称2020年7月19日23时许将电动车停放在太玉园东区42号楼2单元单元楼道内，于7时发现电动车不见了，我所民警英明现场开展工作。经请示值班领导赵志明同意上报。'
    # slice_p = '刘占东先生报在潞城镇侉店村60号底商门口，电动车被盗。（已复核）经出现场了解：报警人称其店内工人刘卫峰（男，身份证：412825198111038518，电话：18500279068）2020年7月19日晚22时许将两轮电动车停放在北京市通州区潞城镇侉子店村60号底商海尔电器门店前，7月20日早6时30分许发现其停放的电动车丢失，目前我所主办民警付海涛已受理此事。该警情经主办民警付海涛、值班警长杨超、值班领导袁振龙核实上报。'
    # slice_p = '刘女士报：在西什库大街北大医院第二住院部东门，电动车被盗。（已复核）12时4分6秒 174号已复核。民警徐岩、孙庆晏到现场经了解是报警人早7时将电瓶车停在西什库大街北大医院第二住院部东门，11时发现不见了，民警正在帮其查看监控后受理。反馈民警：王喆 值班领导：阚建良'
    # slice_p = '李先生报在北辰西路亚丁湾酒店门口，电动车被盗。（已复核）民警宋旭日现场处置，经核实，报警人于本月17日13时许将电动自行车（无发票，白色雅迪电动车，3成新，价格不详）停放在朝阳区俊峰华亭A座东侧路边后离开，今日回来发现车被盗，周边无监控设备。民警已按行政案件受理。属治安类警情，负责勤务指挥副所长王大未同意上报'
    slice_p = '李兆龙报：在管庄杨闸地铁（388路）公交站（往北京进京方向），电动车被盗。但该群众手机号码机主信息提示黄色警示人员，请予以关注并按相关规范开展工作。（已复核）出警民警刘金文赶赴现场经了解，报警人称停放在管庄乡388路公交车站停放的两轮电动车（爱玛牌白色）被盗，现已受理为治安案件，负责勤务指挥领导芦菲同意上报。'

    path = './library/new_situ_pos.json'
    content = load_rules(path)
    single_detect(content, slice_p)
    # bike_demo = demo()
    # bike_demo.run()

