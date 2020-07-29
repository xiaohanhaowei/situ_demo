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

class api_interface():
    
    def __init__(self, label, content):
        self.content = content
        self.type1, self.type2, self.type3 = label.split("_")
        self.type2_3 = "_".join(label.split("_")[1:3])

    def update_content(self, online):
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
        

    def train(self, lable, excel_path):
        '''
        @Author: hongwei.wang
        @date: 2020-07-29
        @func: 
        @args: 
        @return: 
        @raise: 
        '''
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
                if result == self.type2_3 and sub_data_content[19] ==self.type2:
                    compatible_count += 1 

            new_data.append(result)
            new_data.append(reason)
            reason_list.append(reason)
        sheet.insert(ncols, "result", new_data)
        sheet.insert(ncols, 'reason',reason_list)
        # sheet.to_excel('./test_result/result-%s.xls' % excel_path.split('.xls')[0].split('/')[-1], index=False)
        self.new_sheet = pd.DataFrame(sheet, columns=[excel_header[5], excel_header[6], excel_header[18],   excel_header[19], excel_header[20], excel_header[21], 'result', 'reason'])
        #                                        警情摘要          反馈内容           类别1                类别2             类别3              类别4              类别2_类别3  错因
        self.new_sheet.to_excel('./test_result/result.xls')
        accuracy, recall, fpr = self.percision_cal(compatible_count, new_sheet)
        return self.new_sheet, accuracy, recall, fpr

    def percision_cal(self, count, new_sheet):
        '''
        @Author: hongwei.wang
        @date: 2020-07-29
        @func: 
        @args: 
        @return: 
        @raise: 
        '''
        accuracy = 0.
        recall = 0.
        fpr = 0.

        total = new_sheet.shape[0]
        excel_header = new_sheet.columns.tolist()
        TP = len(new_sheet[excel_header[3]] == self.type2 and new_sheet[excel_header[6]].split('_')[0]==self.type2)
        FP = len(new_sheet[excel_header[3]] == self.type2 and new_sheet[excel_header[6]].split('_')[0] == '其他')
        TN = len(new_sheet[excel_header[3]] != self.type2 and new_sheet[excel_header[6]].split('_')[0] == '其他')
        FN = len(new_sheet[excel_header[3]] != self.type2 and new_sheet[excel_header[6]].split('_')[0] == self.type2)
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
    api_interface()