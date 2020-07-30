#curl -H "Content-Type:application/json;charset=utf-8" -X POST -d '{"informations":[{"id":11,"lines":["4971", "", "", "" ,"", "李先生报在北辰西路亚丁湾酒店门口，电动车被盗。（已复核）民警宋旭日现场处置，经核实，报警人于本月17日13时许将电动自行车（无发票，白色雅迪电动车，3成新，价格不详）停放在朝阳区俊峰华亭A座东侧路边后离开，今日回来发现车被盗，周边无监控设备。民警已按行政案件受理。属治安类警情，负责勤务指挥副所长王大未同意上报", "", "" ,"昌平分局", ""]}],"topN":1}' http://127.0.0.1:9010/api/policeaffairs/search

curl -H "Content-Type:application/json;charset=utf-8" -X POST -d '{"informations":[{"id":11,"lines":["4971", "", "", "" ,"", "李先生报在北辰西路亚丁湾酒店门口，电动车被盗。（已复核）民警宋旭日现场处置，经核实，报警人于本月17日13时许将电动自行车（无发票，白色雅迪电动车，3成新，价格不详）停放在朝阳区俊峰华亭A座东侧路边后离开，今日回来发现车被盗，周边无监控设备。民警已按行政案件受理。", "", "" ,"昌平分局", ""]}],"topN":1}' http://127.0.0.1:9010/api/policeaffairs/search

#curl -H "Content-Type:application/json;charset=utf-8" -X POST -d '{"informations":[{"id":11,"lines":["4971", "", "", "" ,"", "宋女士报在北京站北侧永辉超市门口，电动车被盗。", "民警曹小征现场反馈：报警人今日20时许将电动车放在永辉超市门口，21时发现电动车不见了，电动车2015年10月1550元人民币购买，民警处理", "", "" ,"昌平分局", ""]}],"topN":1}' http://127.0.0.1:9010/api/policeaffairs/search

#curl -H "Content-Type:application/json;charset=utf-8" -X POST -d '{"informations":[{"id":11,"lines":["4971", "", "", "" ,"", "宋女士报在北京站北侧永辉超市门口，电动车被盗。", "民警曹小征现场反馈：报警人今日20时许将电动车放在永辉超市门口，21时发现电动车不见了，电动车2015年10月1550元人民币购买，民警处理", "", "" ,"昌平分局", ""]}],"topN":1}' http://localhost:9100/api/policeaffairs/search



#curl -H "Content-Type:application/json;charset=utf-8" -X POST -d '{"informations":[{"id":"40f1c068-68ba-4526-8f2c-c1867a03abb0","lines":["40f1c068-68ba-4526-8f2c-c1867a03abb0","202007279997","2020-07-27 13:30:07","","张先生报在王四营一男子倒地","张先生报：在王四营粮油市场西门南侧200米，有一男子自己骑电动车倒地，现在躺在地上一动不动，耳朵流血，我不敢过去细看，我是路过看见的。\r\n请按三级先期处置并视情提高处置等级。999：30号。（已复核）","同2020072710008件","朝阳","王四营","朝阳分局"]}],"topN":3}' http://localhost:9100/api/policeaffairs/search
