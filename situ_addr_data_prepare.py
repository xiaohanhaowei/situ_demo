# coding=utf-8
'''
construct the json format examples for BERT
'''
import pandas as pd
import os
import json
import math
import copy as cp

# class_mode = 'address'
class_mode = 'situ'

xls_dir = '../dataset/'
# save_path = './or_dataset'
if class_mode == 'situ':
    save_path = './situ_dataset'
elif class_mode == 'address':
    save_path = './addr_dataset'


# TODO: add reading class file procedure
def file_based_class_prepare(file_dir, class_mode):
    '''
    @args: class_mode: value is either 'situ' or 'addr'
    '''
    label_dict = {}
    target_class_file = class_mode + '.txt'
    file = open(os.path.join(file_dir, target_class_file), 'r')
    label_content = file.readlines()
    for index, sub_content in enumerate(label_content):
        sub_content = sub_content.replace('\n', '')
        sub_content = sub_content.strip()
        label_dict[sub_content] = index
    return label_dict


def file_based_dataset_prepare(xls_dir, label_dict, class_mode='addr', save_path='./dataset', mode='train'):
    '''
    use this fn to construct json format example
    args:
        xls_dir: The excel file path
        mode: either var in range of 'train', 'validate' and 'test'
    '''
    log_file = open(os.path.join(save_path, '_'.join([class_mode, mode, 'log.txt'])), 'w')
    if class_mode == 'addr' and label_dict is not None:
        raise TypeError('class mode {}, label_dict must not be None!'.format(class_mode))
    mode = str(mode)
    if mode.lower() not in ('train', 'dev', 'test'):
        raise TypeError('{} is not in range of train, validate, test'.format(mode))
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_file = os.path.join(save_path, mode + '.json')
    index = 0
    f = open(save_file, 'w')
    sheet = pd.read_excel(os.path.join(xls_dir, mode + '.xls'))    
    data = sheet.values
    for sub_data in data:
        sub_data_content = []
        for i in range(2):
            if str(sub_data[5 + i]) == 'nan':
                log_file.write(str(sub_data[0]) + ': the {}th has no content!\n'.format(str(i)))
                continue
            else:
                sub_data[5 + i] = sub_data[5 + i].replace('\n', '')
                sub_data[5 + i] = sub_data[5 + i].replace('\\n', '')
                sub_data[5 + i] = sub_data[5 + i].replace(' ', '')
                sub_data[5 + i] = sub_data[5 + i].replace('\r', '')
                sub_data_content.append(sub_data[5 + i].strip('。'))
        sentence = '；'.join(sub_data_content[:2])
        if mode.lower() in ('train', 'dev'):
            if class_mode == 'addr':
                label_des = sub_data[11]
            elif class_mode == 'situ':
                label_des = sub_data[19]
            else:
                raise ValueError('{} not support'.format(class_mode))
            if str(label_des) == 'nan':
                log_file.write(mode.lower() + '_' + str(sub_data[0]) + ' row has no label!\n')
                continue
            if '其他' in str(label_des):
                label_des = '其他'
            if class_mode == 'addr':
                assert label_des in label_dict.keys(), '{}_{} is not in the labels description'.format(mode, label_des)
            elif class_mode == 'situ':
                if label_des not in label_dict.keys():
                    label_dict[label_des]=len(label_dict)
            else:
                raise ValueError('{} not support'.format(class_mode))
            label = label_dict[label_des]
            json_data = {"label": str(label), "label_des": label_des, "sentence": sentence}
            json_str = json.dumps(json_data, ensure_ascii=False)
            print(json_str)
            f.write(json_str)
            f.write('\n')
        elif mode.lower() == 'test':
            index = int(sub_data[0])
            json_data = {"id": index, "sentence": sentence} 
            json_str = json.dumps(json_data, ensure_ascii=False)
            print(json_str)
            f.write(json_str)
            f.write('\n')
            index += 1           
    f.close()
    log_file.close()
    return label_dict


def file_based_partial_dataset_prepare(xls_dir, label_dict, class_mode='addr', save_path='./dataset', mode='train'):
    '''
    use this fn to construct json format example
    args:
        xls_dir: The excel file path
        mode: either var in range of 'train', 'validate' and 'test'
    '''
    log_file = open(os.path.join(save_path, '_'.join([class_mode, mode, 'log.txt'])), 'w')
    if label_dict is None:
        raise TypeError('class mode {}, label_dict must not be None!'.format(class_mode))
    mode = str(mode)
    if mode.lower() not in ('train', 'dev', 'test'):
        raise TypeError('{} is not in range of train, validate, test'.format(mode))
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_file = os.path.join(save_path, mode + '.json')
    index = 0
    f = open(save_file, 'w')
    sheet = pd.read_excel(os.path.join(xls_dir, mode + '.xls'))    
    data = sheet.values
    for sub_data in data:
        sub_data_content = []
        for i in range(2):
            if str(sub_data[5 + i]) == 'nan':
                log_file.write(str(sub_data[0]) + ': the {}th has no content!\n'.format(str(i)))
                continue
            else:
                sub_data[5 + i] = sub_data[5 + i].replace('\n', '')
                sub_data[5 + i] = sub_data[5 + i].replace('\\n', '')
                sub_data[5 + i] = sub_data[5 + i].replace(' ', '')
                sub_data[5 + i] = sub_data[5 + i].replace('\r', '')
                sub_data_content.append(sub_data[5 + i].strip('。'))
        sentence = ';'.join(sub_data_content[:2])
        if mode.lower() in ('train', 'dev'):
            if class_mode == 'addr':
                label_des = sub_data[11]
            elif class_mode == 'situ':
                label_des = sub_data[19]
            else:
                raise ValueError('{} not support'.format(class_mode))
            if str(label_des) == 'nan':
                log_file.write(mode.lower() + '_' + str(sub_data[0]) + ' row has no label!\n')
                continue
            if '其他' in str(label_des):
                label_des = '其他'
            if label_des not in label_dict.keys():
                continue
            label = label_dict[label_des]
            json_data = {"label": str(label), "label_des": label_des, "sentence": sentence}
            json_str = json.dumps(json_data, ensure_ascii=False)
            print(json_str)
            f.write(json_str)
            f.write('\n')
        elif mode.lower() == 'test':
            index = int(sub_data[0])
            json_data = {"id": index, "sentence": sentence} 
            json_str = json.dumps(json_data, ensure_ascii=False)
            print(json_str)
            f.write(json_str)
            f.write('\n')
            index += 1           
    f.close()
    log_file.close()


'''
def local_based_dataset_prepare(datas, save_path='./dataset', mode='train'):
    mode = str(mode)
    if mode.lower() not in ('train', 'dev', 'test'):
        raise TypeError('{} is not in range of train, validate, test'.format(mode))
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_file = os.path.join(save_path, mode + '.json')
    index = 0
    f = open(save_file, 'w')
    dataset_list = []
    for sub_data in datas:
        for i in range(3):
            sub_data[i] = sub_data[i].strip('。')
        sentence = ';'.join(sub_data[:3])
        if mode.lower() in ('train', 'dev'):
            label_des = sub_data[3]
            assert label_des in label_dict.keys(), '{} is not in the labels description'.format(label_des)
            label = label_dict[label_des]
            json_data = {"label": str(label), "label_des": label_des, "sentence": sentence}
            json_str = json.dumps(json_data, ensure_ascii=False)
            dataset_list.append(json_str)
            print(json_str)
            f.write(json_str)
            f.write('\n')
        elif mode.lower() == 'test':
            index = int(sub_data[0])
            json_data = {"id": index, "sentence": sentence} 
            json_str = json.dumps(json_data, ensure_ascii=False)
            dataset_list.append(json_str)
            print(json_str)
            f.write(json_str)
            f.write('\n')
            index += 1           
    f.close()
    return dataset_list
'''


def _label_des_proc(string):
    string = string.strip()
    string = string.strip('}')
    string = string.strip('{')
    string = string.replace(' ', '')
    string = string.split(':')[-1]
    string = string.strip('"')
    return string


def Save_Label(label_dict, save_path, class_mode='address'):
    f = open(os.path.join(save_path, 'labels.json'), 'w')
    class_f = open(os.path.join(save_path, '{}.txt'.format(class_mode)), 'w')
    for key, value in label_dict.items():
        label_content = {"label": str(value), "label_des": key}
        json_str = json.dumps(label_content, ensure_ascii=False)
        f.write(json_str)
        f.write('\n')
        class_f.write(key)
        class_f.write('\n')
    f.close()
    class_f.close()


def dataset_label_analyse(xls_dir, save_path, mode='all', label_type='situ'):
    label_num_dict = {} 
    label_num_analyse_file = open(os.path.join(save_path, mode+'_analyse.json'), 'w')
    label_file = open(os.path.join(xls_dir, label_type+'.txt'), 'r')
    label_content = label_file.readlines()
    label_list = list(map(_label_des_proc, label_content))
    label_list_c = cp.deepcopy(label_list)
    sheet = pd.read_excel(os.path.join(xls_dir, mode + '.xls'))
    data = sheet.values
    for sub_data in data:
        if label_type == 'address':
            label_des = sub_data[11]
        else:
            label_des = sub_data[19]
        if str(label_des) == 'nan':
            continue
        if '其他' in str(label_des):
            label_des = '其他'
        assert label_des in label_list, '{} is not in the labels description'.format(label_des)
        if label_des in label_list and label_des in label_list_c:
            label_list_c.remove(label_des)
        if label_des not in label_num_dict.keys():
            label_num_dict[label_des] = 1
        else:
            label_num_dict[label_des] += 1
    for item in label_list_c:
        label_num_dict[item] = 0
    for key, value in dict(sorted(label_num_dict.items(), key= lambda x: x[1], reverse=True)).items():
        label_num_cont = {"label_des": str(key), "num": str(value)}
        json_str = json.dumps(label_num_cont, ensure_ascii=False)
        label_num_analyse_file.write(json_str)
        label_num_analyse_file.write('\n')
    label_num_analyse_file.close()


def read_xls(xls_path, class_mode='situ'):
    '''
    @Author: hongwei.wang
    @func: read excels in a centain path and concatenate them
    @return: concatenated excel object
    '''
    all_content = []
    path = xls_path
    xls_files = os.listdir(path)
    files_length = len(xls_files)
    if files_length == 0 or None:
        raise ValueError('{} has no excel file'.format(path))
    paths = [path for num in range(files_length)]
    all_xls_path = map(os.path.join, paths, xls_files)
    for sub_path in all_xls_path:
        excel_ori = pd.read_excel(sub_path)
        all_content.append(excel_ori)
    all_content_concat = pd.concat(all_content)
    print('#'*30)
    print(all_content_concat)
    return all_content_concat


def analyse_xls_content(content, label_dict, class_mode='situ'):
    '''
    @Author: hongwei.wang
    @func: spawn label contents corresponding to different class_mode 
    @return xls values corresponding to different class_mode
    '''
    content_value = content.values
    label_values = []
    for i, label in enumerate(label_dict.keys()):
        if class_mode == 'situ':
            tmp = content_value[content_value[:, 19] == label]
        else:
            tmp = content_value[content_value[:, 11] == label]
        label_values.append(tmp)
    return label_values


def load_values2_json(label_values, label_dict, dataset_dir='./CLUEdataset', class_mode='situ'):
    mode = ('train', 'dev')
    police_type = {'situ': 'police_situation',
                   'addr': 'police_address'}
    if label_dict is None:
        raise TypeError('class mode {}, label_dict must not be None!'.format(class_mode))
    if not os.path.exists(dataset_dir):
        raise NotADirectoryError('has no dataset_dir!')
    for sub_mode in mode:
        log_file = open(os.path.join(dataset_dir, police_type[class_mode], '_'.join([class_mode, sub_mode, 'log.txt'])), 'w')
        data_file_path = os.path.join(dataset_dir, police_type[class_mode], sub_mode + '.json')
        if not os.path.exists(data_file_path):
            raise NotADirectoryError('There is no {}'.format(data_file_path))
        data_file = open(data_file_path, 'a+')
        # data_file.write('\n')
        print('*'*20)
        print(label_values)
        for sub_label in label_values:
            sub_mode_len = int(len(sub_label) * 0.9)
            print(sub_mode, sub_mode_len)
            if sub_mode_len == 0:
                continue
            if sub_mode == 'train':
                cand_data = sub_label[:sub_mode_len+1]
            else:
                cand_data = sub_label[sub_mode_len+1:]
            for sub_data in cand_data:
                sub_data_content = []
                for i in range(2):
                    if str(sub_data[5 + i]) == 'nan':
                        log_file.write(str(sub_data[0]) + ': the {}th has no content!\n'.format(str(i)))
                        continue
                    else:
                        sub_data[5 + i] = sub_data[5 + i].replace('\n', '')
                        sub_data[5 + i] = sub_data[5 + i].replace('\\n', '')
                        sub_data[5 + i] = sub_data[5 + i].replace(' ', '')
                        sub_data[5 + i] = sub_data[5 + i].replace('\r', '')
                        sub_data_content.append(sub_data[5 + i].strip('。'))
                sentence = ';'.join(sub_data_content[:2])
                label_des = sub_data[19] if class_mode == 'situ' else sub_data[11]
                if str(label_des) == 'nan':
                    log_file.write(sub_mode.lower() + '_' + str(sub_data[0]) + ' row has no label!\n')
                    continue
                if '其他' in str(label_des):
                    label_des = '其他'
                if label_des not in label_dict.keys():
                    continue
                label = label_dict[label_des]
                json_data = {"label": str(label), "label_des": label_des, "sentence": sentence}
                json_str = json.dumps(json_data, ensure_ascii=False)
                data_file.write(json_str)
                data_file.write('\n')


if __name__ == '__main__':
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    if class_mode == 'address':
        label_dict = file_based_class_prepare(xls_dir, 'address.txt')
    elif class_mode == 'situ':
        label_dict = {}
    else:
        raise ValueError('class mode {} dose not support!'.format(class_mode))
    label_dict = file_based_class_prepare(xls_dir, class_mode)
    #label_dict = file_based_dataset_prepare(xls_dir, label_dict, class_mode, save_path, mode='train')
    #label_dict = file_based_dataset_prepare(xls_dir, label_dict, class_mode, save_path, mode='dev')
    #file_based_dataset_prepare(xls_dir, label_dict, class_mode, save_path, mode='test')
    Save_Label(label_dict, save_path, class_mode)
    file_based_partial_dataset_prepare(xls_dir, label_dict, class_mode, save_path, mode='train')
    file_based_partial_dataset_prepare(xls_dir, label_dict, class_mode, save_path, mode='dev')
    file_based_partial_dataset_prepare(xls_dir, label_dict, class_mode, save_path, mode='test')

    
    #dataset_label_analyse(xls_dir, save_path, mode='dev',label_type=class_mode)
