# -*- encoding: utf-8 -*-
'''
@Author  :   hongwei.wang 
@File    :   wrapper.py
@Time    :   2020/07/22 13:26:54
@Version :   V1.0
@Contact :   hongwei.wang@lynxi.com
@Desc    :   wrapper the single sentence detectiong function.
'''

import os

import pandas as pd

import classify


def file_based_data_prep(xls_dir, save_path='./log_file'):
    '''
    @Author: hongwei.wang
    @date: 2020-07-22
    @func: 
    @args: 
    @return: data
    @raise: 
    '''
    xls_list = os.listdir(xls_dir)
    quant_list = filter(lambda x: x.split('.')[-1] == 'xls', xls_list)
    if False in quant_list:
        raise ValueError('%s contains elments that is not \'xls\' format')
    xls_dir_list = [xls_dir for i in range(len(xls_list))]
    sentences = []
    for base, sub in zip(xls_dir_list, xls_list):
        log_file = open(os.path.join(save_path, '_'.join([sub.split('.')[0], 'log.txt'])), 'w')
        sheet = pd.read_excel(os.path.join(base, sub))
        data = sheet.values
        for sub_data in data:
            sub_data_content = []
            for i in range(2):
                if str(sub_data[7 + i]) == 'nan':
                    log_file.write(sub + '-' + str(sub_data[0]) + ': the {}th has no content!\n'.format(str(i)))
                    continue
                else:
                    sub_data[7 + i] = sub_data[7 + i].replace('\n', '')
                    sub_data[7 + i] = sub_data[7 + i].replace('\\n', '')
                    sub_data[7 + i] = sub_data[7 + i].replace(' ', '')
                    sub_data[7 + i] = sub_data[7 + i].replace('\r', '')
                    sub_data_content.append(sub_data[7 + i].strip('。'))
            sentence = ';'.join(sub_data_content[:2])
            sentences.append(sentence)
    return sentences


def data_proc(content, xls_file):
    sheet = pd.read_excel(xls_file)
    ncols = sheet.shape[1]
    data = sheet.values
    new_data = list()
    index_list = list()
    for index, sub_data in enumerate(data):
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
            result = '不是盗销自行车-lack-content'
        else:
            result = classify.single_detect(content, sentence)
        new_data.append(result)
        index_list.append(index + 1)
    sheet.insert(ncols, "result", new_data)
    sheet.insert(ncols, 'index', index_list)
    sheet.to_excel('./test_result/result-%s.xls' % xls_file.split('.xls')[0].split('/')[-1], index=False)


if __name__ == "__main__":
    xls_dir = './data/train.xls'
    # xls_dir = './data/test.xls'
    path = './library/new_situ_pos.json'
    content = classify.load_rules(path)
    # single_detect(content, slice_p)
    data_proc(content, xls_dir)
