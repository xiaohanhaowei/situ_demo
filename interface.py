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

import classify
import pandas as pd
import datetime
from collections import OrderedDict

class api_interface(object):
    def __init__(self):
        # self.jsonpath = os.path.join(os.path.dirname(__file__), 'library/new_situ_pos.json')
        # self.labelpath = os.path.join(os.path.dirname(__file__), 'library/label.json')
        self.jsonpath = './library/new_situ_pos_offline.json'
        self.content = self.load_json(self.jsonpath)
        self.json_online = './library/new_situ_pos_online.json'
        self.data_online = OrderedDict()
        self.load_online()

    def update_lib(self):
        self.content = self.load_json(self.jsonpath)

    # 加载json
    def load_json(self, path):
        with open(path, 'r', encoding="utf-8") as json_file:
            content = json.load(json_file)
        return content

    # 加载已上线数据
    def load_online(self):
        if os.path.exists(self.json_online):
            self.data_online = self.load_json(self.json_online)

    # 保存数据到json
    def dump_json(self):
        with open(self.json_online, 'w', encoding="utf-8") as json_file:
            json.dump(self.data_online, json_file, ensure_ascii=False, indent=2)

    # 线上数据类别更新，同步online json
    def update_online(self, type1_type2_="", time=""):
        if type1_type2_:
            self.data_online[type1_type2_] = self.content.get(type1_type2_, {})
            self.data_online[type1_type2_]["time"] = time if time else datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            self.dump_json()

    # 获取已上线的标签和时间
    def update_label_time(self):
        return OrderedDict((key, subdict.get("time", "")) for key, subdict in self.data_online.items())

    # 根据label 获取对应字典
    def from_label_get_dict(self, type1_type2_=""):
        subdict = self.content.get(type1_type2_, {})
        get_dict = dict([(k, subdict.get(k, [])) for k in ["verb", "noun", "overcome"]])
        if type1_type2_ not in self.content:
            self.content[type1_type2_] = get_dict
        return get_dict

    # 根据online 数据 增删本地json数据
    def update_content(self, type1_type2_="", wordlist=[], sign="", time=""):
        '''
        @Author: qikun.zhang
        @date: 2020-07-29
        @func:
        @args:
            content: json instance that need update
            online: the manually updated content that need to update to the json instance
            operation: string type, either 'del' or 'add'
        @return:
        @raise:
        '''

        if type1_type2_:
            subdict = self.content.get(type1_type2_, {})
            for w, worddict in enumerate(wordlist):
                word = worddict.get("kname", "")
                type_ = worddict.get("type", "")
                if type_ not in subdict:
                    subdict[type_] = list()

                words = subdict[type_]
                if sign == "add" and word:
                    words.append(word)
                # elif sign == "del" and word in words and type_ == "overcome":
                elif sign == "del" and word in words:
                    words.remove(word)
                # 去重
                subdict[type_] = list(set(words))
            subdict["time"] = time if time else datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            self.content[type1_type2_] = subdict
            with open(self.jsonpath, 'w', encoding="utf-8") as json_out:
                json.dump(self.content, json_out, ensure_ascii=False, indent=2)
        else:
            print("type1_type2_ is %s, can not find in library" % type1_type2_)


    def update_class_timestamp(self, target_class, t_str):
        '''
        @Author: hongwei.wang
        @date: 2020-07-31 16:42:24
        @func: 
        @args: 
            target_class:
            t_str:       time stamp correspond to the 'y-m-d h:m:s'
        @return: 
        @raise: 
        '''
        sub_dict = self.content.get(target_class, {})
        sub_dict['time'] = t_str
        self.content[target_class] = sub_dict
        with open(self.jsonpath, 'w', encoding="utf-8") as json_out:
            json.dump(self.content, json_out, ensure_ascii=False, indent=2)

    
    def extract_class_timestamp(self):
        online_dict = {}
        keys = list(self.content.keys())
        for sub_class in keys:
            timestamp = self.content[sub_class].get('time', '')
            if timestamp != '':
                online_dict[sub_class] = timestamp   
        return online_dict        


    # added by hongwei.wang
    def train(self, label, excel_path):
        '''
        @Author: hongwei.wang
        @date: 2020-07-29
        @func: 
        @args: 
        @return: 
        @raise: 
        '''
        try:
            length = len(label.split('_'))
            self.label = label
            self.type1, self.type2 = label.split("_")[0:2]
            # self.type2_3 = "_".join(label.split("_")[1:3])

            sheet = pd.read_excel(excel_path)
            excel_header = sheet.columns.tolist()
            print(excel_header)
            ncols = sheet.shape[1]
            data = sheet.values
            new_data = list()
            reason_list = list()
            real_data_list = list()
            eval_list = list()
            compatible_count = 0
            if len(data) == 0:
                raise ValueError('excel表中没有数据，请添加新的excel!')
            for sub_data in data:
                sub_data_content = []
                valid_label = list(map(lambda x: str(x), sub_data[18:].tolist()))
                valid_label_set = set(valid_label)
                if 'nan' in valid_label_set:
                    valid_label_set.remove('nan')
                valid_label_new = list(valid_label_set)
                valid_label_new.sort(key=valid_label.index)
                valid_len = len(valid_label_new)
                # 预防实际标签为空的情况
                if valid_len == 0:
                    sub_real_data = '未知'
                elif valid_len > 0 and valid_len != length:
                    sub_real_data = '其他'
                else:
                    if '_'.join(valid_label_new[:]) not in label:
                        sub_real_data = '其他'
                    else:
                        sub_real_data = label
                for i in range(2):
                    if str(sub_data[5 + i]) == 'nan':
                        break
                    else:
                        sub_data[5 + i] = sub_data[5 + i].replace('\n', '')
                        sub_data[5 + i] = sub_data[5 + i].replace('\\n', '')
                        sub_data[5 + i] = sub_data[5 + i].replace(' ', '')
                        sub_data[5 + i] = sub_data[5 + i].replace('\r', '')
                        sub_data_content.append(sub_data[5 + i].strip('。'))
                # FIXME: Check if the content is blank!!
                sentence = '；'.join(sub_data_content[:2])
                if len(sub_data_content) != 2:
                    result = '其他'
                    reason = 'no_content'
                else:

                    result, reason = classify.single_detect_for_analyse(self.content, label, sentence)
                    if '_' in result:
                        if result.split('_')[1] == self.type2 and sub_data[19] == self.type2:
                            compatible_count += 1 
                if '_' in result: # the result is only the name of label
                    if sub_real_data == '未知':
                        eval = 'unknown'
                    elif sub_real_data == label: 
                        eval = 'True'
                    else:
                        eval = 'False'
                else: #其他
                    if sub_real_data == '未知':
                        eval = 'unknown'
                    elif  sub_real_data == label: 
                        eval = 'False'
                    else:
                        eval = 'True'
                new_data.append(result)
                reason_list.append(reason)
                real_data_list.append(sub_real_data)
                eval_list.append(eval)
            # sheet['result'] = pd.Series(new_data)
            # sheet['reason'] = pd.Series(reason_list)

            sheet.insert(ncols, "result", new_data)
            sheet.insert(ncols+1, "evaluate", eval_list)
            sheet.insert(ncols+2, "reason", reason_list)
            sheet.insert(ncols+3, 'real_data', real_data_list)
            # sheet.to_excel('./static/result-%s.xls' % excel_path.split('.xls')[0].split('/')[-1], index=False)
            self.new_sheet = pd.DataFrame(sheet,
                columns=[excel_header[5], excel_header[6], excel_header[18], excel_header[19], excel_header[20],
                    excel_header[21], 'result', 'evaluate', 'reason', 'real_data'])
            #                 警情摘要          反馈内容           类别1                类别2             类别3              类别4              类别2_类别3  错因
            self.new_sheet.to_excel('./static/result.xls')

            new_sheet1 = self.new_sheet[self.new_sheet['evaluate'] == 'True']
            new_sheet1.to_excel('./static/result-true.xls')

            new_sheet1 = self.new_sheet[self.new_sheet['evaluate'] == 'False']
            new_sheet1.to_excel('./static/result-false.xls')

            accuracy, fake_accuracy, other_accuracy, fpr, indicit_l = self.percision_cal(label, compatible_count)

            # return self.new_sheet, accuracy, recall, fpr
            return {# 'data': self.new_sheet.to_json(force_ascii=False),
                    'indict': {
                        'c-len': int(indicit_l[-2]),  # lable_num 应正确数
                        'c-correct': int(indicit_l[0]),  # TP  推理正确数
                        'c-accuracy': fake_accuracy,  # 推理准确率
                        'o-len': int(indicit_l[-1]),  # other_num 应其他数
                        'o-correct': int(indicit_l[1]),  # TN 推理其他数
                        'o-accuracy': other_accuracy,  # 其他准确率
                        'fpr': fpr  # 误报率
                        }
                    }
        except Exception as e:
            print(e)


    def percision_cal(self, label, count):
        '''
        @Author: hongwei.wang
        @date: 2020-07-29
        @func: 
        @args: 
        @return: 
        @raise: 
        '''
        new_sheet = self.new_sheet
        accuracy = 0.
        recall = 0.
        fpr = 0.

        # total = new_sheet.shape[0]
        excel_header = new_sheet.columns.tolist()
        # ['警情摘要', '反馈内容', '警情类别1(总队)', '警情类别2(总队)', '警情类别3(总队)', '警情类别4(总队)', 
        # 'result', 'evaluate', 'reason', 'real_data']
        ee = new_sheet[excel_header[3]].tolist()  # 实际的 FIXME have a bug
        dd = new_sheet[excel_header[2:6]].values.tolist() # 真正实际的总数

        # fake accuracy calculate
        hh = [label for data in new_sheet[excel_header[3]]]
        def str_list(x):
            return list(map(lambda i:str(i), x))
        dd = list(map(str_list, dd))
        cc = ['_'.join(x) for x in dd] #把类别1到类别4连起来 肯定会有bug
        label_num = [x in y for x, y in zip(hh, cc)].count(True)

        # print(new_sheet[excel_header[6]].tolist())
        # 以下对比只对比了type2
        # ===========================
        # ff = list(map(lambda x: x.split('_')[0] if '_' not in x else x.split('_')[1], new_sheet[excel_header[6]].tolist()))  # 推理的
        # gg = [self.type2 for data in new_sheet[excel_header[3]]]
        # tt = list(map(lambda x, y: x == y, ee, gg))  # 实际为真
        # ti = list(map(lambda x, y: x == y, ff, gg))  # 推理为真
        # ============================

        # 以下对比为对比全类别
        # ============================
        benchmark_sheet = new_sheet[new_sheet['real_data'] != '未知']
        total = benchmark_sheet.shape[0]
        tt = list(map(lambda x: x == label, benchmark_sheet['real_data'].values.tolist()))  # 实际为真 filter this column of content
        ti = list(map(lambda x: x == label, benchmark_sheet['result'].values.tolist()))# 推理为真
        other_num = new_sheet[new_sheet['real_data'] == '其他'].shape[0]
        # ============================

        TP = sum([x == True and y == True for x, y in zip(ti, tt)])
        TN = sum([x == False and y == False for x, y in zip(ti, tt)])
        FP = sum([x == True and y == False for x, y in zip(ti, tt)])
        FN = sum([x == False and y == True for x, y in zip(ti, tt)])
        # TP = len(new_sheet[excel_header[3]].tolist() == [self.type2 for data in new_sheet[excel_header[3]]] and list(map(lambda x: x.split('_')[0], new_sheet[excel_header[6]].tolist())) == [self.type2 for data in new_sheet[excel_header[6]]])
        # FP = len(new_sheet[excel_header[3]] == self.type2 and new_sheet[excel_header[6]].split('_')[0] == '其他')
        # TN = len(new_sheet[excel_header[3]] != self.type2 and new_sheet[excel_header[6]].split('_')[0] == '其他')
        # FN = len(new_sheet[excel_header[3]] != self.type2 and new_sheet[excel_header[6]].split('_')[0] == self.type2)
        fake_accuracy = 0 if label_num==0 else float(TP) / label_num * 100
        accuracy = float(float((TP + TN) / total)) * 100
        other_accuracy = 0 if other_num==0 else float(TN) / other_num * 100
        recall = 0 if (TP + FN) == 0 else float(TP / (TP + FN)) * 100
        # fpr = 0 if len(new_sheet[excel_header[3]] != self.type2) == 0 else float(FN / len(new_sheet[excel_header[3]] != self.type2))
        fpr = 0 if (FP + TN) == 0 else float(FP / (FP + TN)) * 100
        return accuracy, fake_accuracy, other_accuracy, fpr, [TP, TN, FP, FN, label_num, other_num]


    def query_data(self):
        '''
        @Author: hongwei.wang
        @date: 2020-07-31
        @func: 
        @args: 
        @return: 
        @raise: 
        '''
        return self.new_sheet


    def filter_content(self, criterion='all'):
        '''
        @Author: hongwei.wang
        @date: 2020-08-01 15:41:48
        @func: 
        @args:
            criterion: 'all'; 'True'; 'False' 
        @return: 
        @raise: 
        '''
        if criterion == 'True':
            new_sheet1 = self.new_sheet[self.new_sheet['evaluate'] == 'True']
            new_sheet1.to_excel('./static/result-true.xls')
            return new_sheet1
        if criterion == 'False':
            new_sheet1 = self.new_sheet[self.new_sheet['evaluate'] == 'False']
            new_sheet1.to_excel('./static/result-false.xls')
            return new_sheet1
        else:
            return self.new_sheet
        

    def compatible_word_sentence(self, label, index):
        return list(self.new_sheet.loc[index, 'reason'])


    def obtain_sheet_slice(self, index, interval, criterion='all'):
        '''
        @Author: hongwei.wang
        @date: 2020-07-31
        @func: 
        @args: 
        @return: 
        @raise: 
        '''
        l_new_sheet = self.filter_content(criterion)
        slice_sheet = l_new_sheet[index: index + interval]
        total = l_new_sheet.shape[0]
        return slice_sheet.to_json(force_ascii=False), total


if __name__ == "__main__":
    # api_interface()
    infer = api_interface()
    # print("infer.content", infer.content)

    # kun's test
    # print("from_label_get_dict", infer.from_label_get_dict("公共秩序管理类_盗销自行车_电动车"))
    #
    # infer.update_content(
    #     type1_type2_="公共秩序管理类_盗销自行车_电动车",
    #     wordlist=[{"kname": "取消报警####", "type": "overcome"}],
    #     sign="add")
    #
    # infer.update_content(
    #     type1_type2_="公共秩序管理类_盗销自行车_电动车",
    #     wordlist=[{"kname": "山地车####", "type": "noun"}],
    #     sign="add")
    #
    # infer.update_content(
    #     type1_type2_="公共秩序管理类_盗销自行车_电动车",
    #     wordlist=[{"kname": "取消报警####", "type": "overcome"}],
    #     sign="del")
    #
    # infer.update_content(
    #     type1_type2_="公共秩序管理类_盗销自行车_电动车",
    #     wordlist=[{"kname": "山地车####", "type": "noun"}],
    #     sign="del")
    #
    # infer.update_online(type1_type2_="公共秩序管理类_盗销自行车_电动车")
    # infer.update_online(type1_type2_="公共秩序管理类_盗销自行车_自行车")
    # print("update label and time", infer.update_label_time())



    # my test
    # print(infer.extract_class_timestamp())
    # infer.update_class_timestamp("公共秩序管理类_盗销自行车_电动车", '2020-07-31 16:53:58')
    # print(infer.train("公共秩序管理类_医院号贩子", './test.xls'))
    print(infer.train("公共秩序管理类_盗销自行车_电动车", './test.xls'))
