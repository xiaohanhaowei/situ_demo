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
        topN = request.json["topN"]

        logger.info(request.data.decode(encoding='utf-8'))

        datas = []
        for info in informations:
            id = info["id"]
            line_list = info["lines"]
            if len(line_list) < 9:
                res['code'] = 10000
                res['message'] = "lines count is less than 9"
                return jsonify(res)

            sentence = line_list[5] + line_list[6]
            data = once_forever(sentence)
            datas.append(data)

        res["data"] = datas

    except Exception as e:
        if hasattr(e, "error_code") and e.error_code != 0:
            res["code"] = e.error_code
            res["message"] = e.msg
        else:
            res["code"] = 10000
            res["message"] = str(e)
    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9100, debug=False)
