curl -H "Content-Type:application/json;charset=utf-8" -X POST -d '{"informations":[{"id":11,"lines":["4971", "", "", "" ,"", "一男子报在燕丹村南口465公交车站反映有很多黑车，请按规定使用执法记录仪到现场开展工作。", "报警人反映七星路有很多黑车堵路，协调相关部门处理。", "", "" ,"昌平分局", ""]}],"topN":1}' http://192.168.11.220:9100/api/policeaffairs/search

# curl -H "Content-Type:application/json;charset=utf-8" -X POST -d '{"informations":[{"id":11,"lines":["4971", "", "", "" ,"", "一男子报在燕丹村南口465公交车站反映有很多黑车，请按规定使用执法记录仪到现场开展工作。", "报警人反映七星路有很多黑车堵路，协调相关部门处理。", "", "" ,"昌平分局", ""]}],"topN":1}' http://localhost:9100/api/policeaffairs/searchbert
