from flask import Flask, request, jsonify

from classify import once_forever
from common import logging

app = Flask(__name__)

logger = logging.LoadLogging('./log_cfg.yml')


@app.route('/api/policeaffairs/search', methods=['GET', 'POST'])
def search():
    res = {
        "code": 0,
        "message": "",
    }

    try:
        informations = request.json['informations']

        logger.info(request.data.decode(encoding='utf-8'))

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
            data = once_forever(sentence)
            data["address"] = {}
            data_res.update(data)
            datas.append(data_res)

        res["data"] = datas
    except Exception as e:
        if hasattr(e, "error_code") and e.error_code != 0:
            res["code"] = e.error_code
            res["message"] = e.msg
        else:
            res["code"] = 10000
            res["message"] = str(e)

    return jsonify(res)
