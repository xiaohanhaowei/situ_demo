import datetime
from datetime import time
from flask import Flask, request, jsonify, Response, render_template
from classify import once_forever, update_lib
from werkzeug.utils import secure_filename
from interface import api_interface
import json
from flask_docs import ApiDoc
import shutil

# app = Flask(__name__)
app = Flask(__name__, static_folder='./static', static_url_path='', template_folder='./static')

ApiDoc(app)
app.config["API_DOC_MEMBER"] = ['api']

json_path = './library/label.json'
json_path_total = './library/label_total.json'
upload_name = ''

infer = api_interface()


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/api/policeaffairs/search', methods=['GET', 'POST'])
def search():
    res = {
        "code": 0,
        "message": "",
    }

    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        check_date()
        informations = request.json['informations']

        datas = []
        for info in informations:
            id = info["id"]
            data_res = {}
            data_res['id'] = id
            line_list = info["lines"]
            if len(line_list) < 9:
                res['code'] = 10000
                res['message'] = "lines count is less than 9"
                return jsonify(res)

            sentence = line_list[5] + "；" + line_list[6]  # BUG
            print("[INFO]: 开始进行调用推理功能 once_forever")
            data = once_forever(sentence)
            print("[INFO]: 完成进行调用推理功能 once_forever")
            data["address"] = {}
            data_res.update(data)
            datas.append(data_res)

        res["data"] = datas
        print("[result]:", datas)

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])
    return jsonify(res)


@app.route('/api/upload', methods=['POST'])
def upload():
    """上传文件

    @@@

    @@@
    """
    res = {
        "code": 0,
        "message": "",
        "data": {},
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        file = request.files.get('file')

        # upload_path = "./upload/" + secure_filename(file.filename)
        upload_path = "./upload/" + secure_filename("test.xls")
        file.save(upload_path)

        upload_name = upload_path

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])
        return jsonify(res)

    return jsonify(res)


@app.route('/api/download', methods=['POST'])
def download():
    """下载文件

    @@@

    @@@
    """
    res = {
        "code": 0,
        "message": "",
        "data": {},
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))

        res["data"] = "/result.xls"

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])
        return jsonify(res)

    return jsonify(res)


@app.route('/api/train', methods=['POST'])
def train():
    """ 训练

    @@@
    #### body参数[json格式]

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    label    |    false    |    string  |    标签 (公共秩序管理类_盗销自行车_电动车)（盗销自行车_ 电动车 、 盗销自行车_自行车）    |

    #### example

    #### return
    - ##### json
    {"message": "", "code": 0, "data":{}}
    {"result":[],
    "acc": {}
    }
    #### example
    ```

    ```
    @@@
    """
    res = {
        "code": 0,
        "message": "",
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        label = request.json["label"]
        excel_path = "./upload/test.xls"

        print("[INFO]:开始调用训练接口 infer.train")

        data = infer.train(label, excel_path)

        print("[INFO]:完成调用训练接口 infer.train 参数：label，", label)
        print("[data]: ", data)

        res["data"] = data

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])

    return response(res)


@app.route('/api/results', methods=['GET'])
def search_result():
    """ 查询结果

    @@@
    #### query参数[json格式]

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    label    |    false    |    string  |    标签    |
    |    appraise    |    false    |    string  |    推理评价    |
    |    resultType    |    false    |    string  |    推理结果    |
    |    pageIndex    |    false    |    int  |    索引页    |
    |    pageSize    |    false    |    int  |    推理结果    |

    #### example

    #### return
    - ##### json
    {"message": "", "code": 0, "data":{}}
    {"result":[]
    }
    #### example
    ```

    ```
    @@@
    """
    res = {
        "code": 0,
        "message": "",
    }

    try:
        print("[request]:", request.data.decode(encoding='utf-8'))

        label = request.args.get('label')
        appraise = request.args.get('appraise')
        result_type = request.args.get('resultType')
        pageIndex = int(request.args.get('pageIndex'))
        pageSize = int(request.args.get('pageSize'))
        print("result_type=", result_type, "pageIndex=", str(pageIndex), "pageSize=", pageSize)

        datas = []

        print("[INFO]: 开始调用推理结果 infer.obtain_sheet_slice")

        page = (pageIndex - 1) * pageSize

        if result_type is None or result_type == "":
            result_type = "all"

        print("result_type=", result_type, "page=", str(page), "pageSize=", pageSize)

        datas = infer.obtain_sheet_slice(page, pageSize, result_type)

        print("[INFO]: 完成调用推理结果 infer.obtain_sheet_slice")

        res["data"] = datas
        print("[result]:", datas)

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])
    return jsonify(res)


@app.route('/api/online/list', methods=['GET'])
def online_list():
    """上线

    @@@
    #### example

    #### return
    - ##### json
    {"message": "", "code": 0}

    #### example
    ```

    ```
    @@@
    """
    res = {
        "code": 0,
        "message": "",
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))

        print("开始获取上线标签, ")

        data = infer.extract_class_timestamp()

        print("完成获取上线标签, ")

        res["data"] = data

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])

    return jsonify(res)


@app.route('/api/online', methods=['POST'])
def online():
    """上线

    @@@
    #### body参数[json格式]

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    label    |    false    |    string  |    标签    |

    #### example

    #### return
    - ##### json
    {"message": "", "code": 0}

    #### example
    ```

    ```
    @@@
    """
    res = {
        "code": 0,
        "message": "",
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))

        label = request.json["label"]

        source_file = "./library/new_situ_pos.json"
        source_file_bak = "./library/new_situ_pos_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json"
        shutil.copy(source_file, source_file_bak)
        offline_file = "./library/new_situ_pos_offline.json"
        shutil.copy(offline_file, source_file)

        print("开始重新加载线上库")
        update_lib()
        print("完成重新加载线上库")
        # 更新时间
        print("开始更新标签时间")

        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        infer.update_class_timestamp(label, time_str)

        print("完成更新标签时间")

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])

    return jsonify(res)


@app.route('/api/pull', methods=['POST'])
def pull():
    """上线

    @@@
    #### example

    #### return
    - ##### json
    {"message": "", "code": 0}

    #### example
    ```

    ```
    @@@
    """
    res = {
        "code": 0,
        "message": "",
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        source_file = "./library/new_situ_pos.json"
        target_file = "./library/new_situ_pos_offline.json"
        shutil.copy(source_file, target_file)

        update_lib()

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])

    return jsonify(res)


@app.route('/api/words', methods=['GET'])
def get_keywords():
    """获取相关词

    @@@
    #### body参数[json格式]

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    label    |    false    |    string  |    标签 (公共秩序管理类_盗销自行车_电动车)（盗销自行车_ 电动车 、 盗销自行车_自行车）    |

    #### example

    #### return
    - ##### json
    {"message": "", "code": 0, "data":{}}
    [{"kname":"电动车", "type":"noun"},
                {"kname":"被偷", "type":"verb"},
                {"kname": "取消报警", "type": "overcome"},
                {"kname": "不属我所管辖", "type": "overcome"}
            ]

    #### example
    ```

    ```
    @@@
    """
    res = {
        "code": 0,
        "message": "",
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))

        label = request.args.get('label')

        print("[INFO]: 开始调用获取相关词接口 infer.from_label_get_dict")

        data = infer.from_label_get_dict(label)

        print("[INFO]: 完成调用获取相关词接口 infer.from_label_get_dict")

        res["data"] = data
        print("[result]:", data)

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)
        print("[Error]:", "code:", res["code"], ", message:", res["message"])
    return response(res)


@app.route('/api/words', methods=['POST'])
def add_keywords():
    """添加相关词

    @@@
    #### body参数[json格式]

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    label    |    false    |    string  |    标签 (公共秩序管理类_盗销自行车_电动车)（盗销自行车_ 电动车 、 盗销自行车_自行车）    |
    |    keyinfos    |    false    |    keyinfo[]  |    信息    |

    ##### keyinfo
    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    kname    |    false    |    string  |    关键词    |
    |    type    |    false    |    string  |    类型（verb、noun、group、overcome）    |

    #### example
    ```
    label: 公共秩序管理类_盗销自行车_电动车
    keyinfo[]
    [{"kname":"电动车", "type":"noun"},
        {"kname":"被偷", "type":"verb"},
        {"kname": "取消报警", "type": "overcome"},
        {"kname": "不属我所管辖", "type": "overcome"}
    ]
    ```

    #### return
    - ##### json
    {"message": "", "code": 0}

    #### example
    ```

    ```
    @@@
    """
    res = {
        "code": 0,
        "message": "",
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        label = request.json["label"]
        keyinfos = request.json["keyinfos"]
        oper_type = "add"

        online = {}
        online[label] = keyinfos

        print("[INFO]: 开始调用添加相关词接口 infer.update_content")

        infer.update_content(label, keyinfos, oper_type)

        print("[INFO]: 完成调用添加相关词接口 infer.update_content")

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])
    return jsonify(res)


@app.route('/api/words', methods=['DELETE'])
def del_keywords():
    """删除相关词

    @@@
    #### body参数[json格式]

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    label    |    false    |    string  |    标签 (公共秩序管理类_盗销自行车_电动车)（盗销自行车_ 电动车 、 盗销自行车_自行车）    |
    |    keyinfos    |    false    |    keyinfo[]  |    信息    |

    ##### keyinfo
    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    kname    |    false    |    string  |    关键词    |
    |    type    |    false    |    string  |    类型（verb、noun、group、overcome）    |

    #### example
    ```
    label: 公共秩序管理类_盗销自行车_电动车
    keyinfo[]
    [{"kname":"电动车", "type":"noun"},
        {"kname":"被偷", "type":"verb"},
        {"kname": "取消报警", "type": "overcome"},
        {"kname": "不属我所管辖", "type": "overcome"}
    ]
    ```

    #### return
    - ##### json
    {"message": "", "code": 0}

    #### example
    ```

    ```
    @@@
    """
    res = {
        "code": 0,
        "message": "",
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        label = request.json["label"]
        keyinfos = request.json["keyinfos"]
        oper_type = "del"

        # online = {
        #     "公共秩序管理类_盗销自行车_电动车":
        #         [{"kname": "电动车", "type": "noun"},
        #          {"kname": "被偷", "type": "verb"},
        #          {"kname": "取消报警", "type": "overcome"},
        #          {"kname": "不属我所管辖", "type": "overcome"}
        #          ]
        # }

        print("[INFO]: 开始调用删除相关词接口 infer.update_content")

        infer.update_content(label, keyinfos, oper_type)

        print("[INFO]: 完成调用删除相关词接口 infer.update_content")

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])
    return jsonify(res)


@app.route('/api/words/unrelated', methods=['GET'])
def get_unrelated():
    """获取一句话的非相关词

    @@@
    #### query参数[json格式]

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    label    |    false    |    string  |    标签 (公共秩序管理类_盗销自行车_电动车)（盗销自行车_ 电动车 、 盗销自行车_自行车）    |
    |    sentence    |    false    |    string  |    句子    |
    |    index    |    false    |    int  |    索引    |


    #### example

    #### return
    - ##### json
    {"message": "", "code": 0}

    #### example
    ```

    ```
    @@@
    """
    res = {
        "code": 0,
        "message": "",
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))

        index = request.args.get('index')
        label = request.args.get('label')
        sentence = request.args.get('sentence')

        print("[INFO]: 开始调用删除相关词接口 infer.compatible_word_sentence")

        infer.compatible_word_sentence(index=index)

        print("[INFO]: 完成调用删除相关词接口 infer.compatible_word_sentence")

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)

        print("[Error]:", "code:", res["code"], ", message:", res["message"])
    return jsonify(res)


@app.route('/api/labels', methods=['GET'])
def get_all_labels():
    res = {
        "code": 0,
        "message": "",
    }
    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        data = load_label(json_path_total)
        type_dict = {}
        type_dict["type1"] = data["type1"]
        type_dict["type2"] = data["type2"]
        type_dict["type3"] = data["type3"]
        type_dict["type4"] = data["type4"]
        type_dict["type5"] = data["type5"]

        res["data"] = type_dict
        print("[result]:", type_dict)
    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)
        print("[Error]:", "code:", res["code"], ", message:", res["message"])

    return response(res)


@app.route('/api/labels/type1', methods=['GET'])
def get_type1():
    res = {
        "code": 0,
        "message": "",
    }

    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        data = load_label(json_path)
        res["data"] = data['type1']
        print("[result]:", data['type1'])

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)
        print("[Error]:", "code:", res["code"], ", message:", res["message"])

    return response(res)


@app.route('/api/labels/type2', methods=['GET'])
def get_type2():
    res = {
        "code": 0,
        "message": "",
    }

    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        key = request.args.get('key')
        data = load_label(json_path)

        results = []
        if key in data['type2'].keys():
            results = data['type2'][key]

        res["data"] = results
        print("[result]:", results)

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)
        print("[Error]:", "code:", res["code"], ", message:", res["message"])

    return response(res)


@app.route('/api/labels/type3', methods=['GET'])
def get_type3():
    res = {
        "code": 0,
        "message": "",
    }

    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        key = request.args.get('key')
        data = load_label(json_path)

        type3_data = {}
        if key in data['type3'].keys():
            type3_data = data['type3'][key]

        results = []
        for d in type3_data:
            result = {}
            result["name"] = d
            result["key"] = type3_data[d]
            results.append(result)
        res["data"] = results
        print("[result]:", results)

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)
        print("[Error]:", "code:", res["code"], ", message:", res["message"])

    return response(res)


@app.route('/api/labels/type4', methods=['GET'])
def get_type4():
    res = {
        "code": 0,
        "message": "",
    }

    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        key = request.args.get('key')
        data = load_label(json_path)

        type4_data = {}
        if key in data['type4'].keys():
            type4_data = data['type4'][key]

        results = []
        for d in type4_data:
            result = {}
            result["name"] = d
            result["key"] = type4_data[d]
            results.append(result)
        res["data"] = results
        print("[result]:", results)

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)
        print("[Error]:", "code:", res["code"], ", message:", res["message"])

    return response(res)


@app.route('/api/labels/type5', methods=['GET'])
def get_type5():
    res = {
        "code": 0,
        "message": "",
    }

    try:
        print("[request]:", request.data.decode(encoding='utf-8'))
        key = request.args.get('key')
        data = load_label(json_path)

        type4_data = {}
        if key in data['type5'].keys():
            type4_data = data['type5'][key]

        results = []
        for d in type4_data:
            result = {}
            result["name"] = d
            result["key"] = type4_data[d]
            results.append(result)
        res["data"] = results
        print("[result]:", results)

    except Exception as e:
        res["code"] = 10000
        res["message"] = str(e)
        print("[Error]:", "code:", res["code"], ", message:", res["message"])

    return response(res)


def response(res):
    return Response(json.dumps(res, indent=2, ensure_ascii=False) + "\n", mimetype="application/json")


def load_label(file_path='./library/label.json'):
    data = None

    with open(file_path) as f:
        data = json.load(f, encoding='utf-8')  # js是转换后的字典
    return data


def now():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def check_date():
    s = '2021-01-01'
    current = now()
    if current > s:
        raise Exception("已过期,无法正常使用")


if __name__ == '__main__':
    check_date()
    app.run(host="0.0.0.0", port=5001, debug=True)
