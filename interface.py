# -*- encoding: utf-8 -*-
'''
@Author  :   hongwei.wang 
@File    :   interface.py
@Time    :   2020/07/29 10:09:58
@Version :   V1.0
@Contact :   hongwei.wang@lynxi.com
@Desc    :   None
'''
import pandas as pd
import classify
import json
import os

class api_interface():
    
    def __init__(self):
        
        
        self.jsonpath = os.path.join(os.path.dirname(__file__), 'library/new_situ_pos.json')
        # self.jsonpath = './library/new_situ_pos.json'
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
        if "_" in type1_type2_:
            type2_ = "_".join(type1_type2_.split("_")[1:])
            if type2_ not in self.content:
                self.content[type2_] = {}
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
                    # elif sign == "del" and word in words and type_ == "overcome":
                    elif sign == "del" and word in words:
                        words.remove(word)
                    subdict[type_] = list(set(words))
                    self.content[type2_] = subdict
            with open(self.jsonpath, 'w', encoding="utf-8") as json_out:
                json.dump(self.content, json_out, ensure_ascii=False, indent=2)
        else:
            print("%s not in situ library, can not update content" % type1_type2_)


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
        self.type1, self.type2, self.type3, _ = label.split("_")
        self.type2_3 = "_".join(label.split("_")[1:3])

        sheet = pd.read_excel(excel_path)
        excel_header = sheet.columns.tolist()
        print(excel_header)
        ncols = sheet.shape[1]
        data = sheet.values
        new_data = list()
        reason_list = list()
        compatible_count = 0
        for sub_data in data:
            sub_data_content = []
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
            sentence = ';'.join(sub_data_content[:2])
            if len(sub_data_content) != 2:
                result = '其他'
                reason = 'no_content'
            else:
                
                result, reason = classify.single_detect_for_analyse(self.content, self.type2_3, sentence)
                if result == self.type2_3 and sub_data[19] ==self.type2:
                    compatible_count += 1 
            
            new_data.append(result)
            reason_list.append(reason)
        # sheet['result'] = pd.Series(new_data)
        # sheet['reason'] = pd.Series(reason_list)

        sheet.insert(ncols, "result", new_data)
        sheet.insert(ncols, 'reason',reason_list)
        # sheet.to_excel('./result-%s.xls' % excel_path.split('.xls')[0].split('/')[-1], index=False)
        self.new_sheet = pd.DataFrame(sheet, columns=[excel_header[5], excel_header[6], excel_header[18],   excel_header[19], excel_header[20], excel_header[21], 'result', 'reason'])
        #                                        警情摘要          反馈内容           类别1                类别2             类别3              类别4              类别2_类别3  错因
        self.new_sheet.to_excel('./result.xls')
        accuracy, recall, fpr = self.percision_cal(compatible_count)
        return self.new_sheet, accuracy, recall, fpr

    def percision_cal(self, count):
        '''
        @Author: hongwei.wang
        @date: 2020-07-29
        @func: 
        @args: 
        @return: 
        @raise: 
        '''
        new_sheet = self.new_sheet
        accuracy = 0.93
        recall = 0.87
        fpr = 0.2

        total = new_sheet.shape[0]
        excel_header = new_sheet.columns.tolist()
        ee = new_sheet[excel_header[3]].tolist()  #实际的
        ff = list(map(lambda x: x.split('_')[0], new_sheet[excel_header[6]].tolist()))  #推理的
        gg =[self.type2 for data in new_sheet[excel_header[3]]]
        tt = list(map(lambda x, y : x ==y, ee, gg))  #实际为真
        ti = list(map(lambda x, y : x ==y, ff, gg))  #推理为真

        TP = sum([x==True and y==True for x, y in zip(tt,ti)])
        FP = sum([x==True and y==False for x, y in zip(tt,ti)])
        TN = sum([x==False and y==False for x, y in zip(tt,ti)])
        FN = sum([x==False and y==True for x, y in zip(tt,ti)])
        # TP = len(new_sheet[excel_header[3]].tolist() == [self.type2 for data in new_sheet[excel_header[3]]] and list(map(lambda x: x.split('_')[0], new_sheet[excel_header[6]].tolist())) == [self.type2 for data in new_sheet[excel_header[6]]])
        # FP = len(new_sheet[excel_header[3]] == self.type2 and new_sheet[excel_header[6]].split('_')[0] == '其他')
        # TN = len(new_sheet[excel_header[3]] != self.type2 and new_sheet[excel_header[6]].split('_')[0] == '其他')
        # FN = len(new_sheet[excel_header[3]] != self.type2 and new_sheet[excel_header[6]].split('_')[0] == self.type2)
        accuracy = float(float((TP + TN) / total))
        recall = float(count / len(new_sheet[excel_header[3]] == self.type2))
        fpr = float(TN / len(new_sheet[excel_header[3]] != self.type2))
        return accuracy, recall, fpr

    def query_data(self):
        '''
        @Author: hongwei.wang
        @date: ${date (Ctrl+Shift+I)}
        @func: 
        @args: 
        @return: 
        @raise: 
        '''
        return self.new_sheet

    def compatible_word_sentence(self, label, index):
        return list(self.new_sheet.loc[index, 'reason'])


if __name__ == "__main__":
    # api_interface()
    infer = api_interface('公共秩序管理类_盗销自行车_电动车')
    print("infer.content", infer.content)
    # kun's test
    # print("from_label_get_dict", infer.from_label_get_dict("公共秩序管理类_盗销自行车_电动车"))

    # infer.update_content(
    #     type1_type2_="公共秩序管理类_盗销自行车_电动车",
    #     wordlist=[{"kname": "取消报警####", "type": "overcome"}],
    #     sign="add")

    # infer.update_content(
    #     type1_type2_="公共秩序管理类_盗销自行车_电动车",
    #     wordlist=[{"kname": "山地车####", "type": "noun"}],
    #     sign="add")

    # infer.update_content(
    #     type1_type2_="公共秩序管理类_盗销自行车_电动车",
    #     wordlist=[{"kname": "取消报警####", "type": "overcome"}],
    #     sign="del")
    #
    # infer.update_content(
    #     type1_type2_="公共秩序管理类_盗销自行车_电动车",
    #     wordlist=[{"kname": "山地车####", "type": "noun"}],
    #     sign="del")
    # my test
    infer.train('./test.xls')
