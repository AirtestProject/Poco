# coding=utf-8

from poco.drivers.windows import WindowsPoco
import time
import json
import base64


poco = WindowsPoco({"handle":198556})

poco(u'树视图').child(u'桌面').child(u'此电脑').offspring(u'桌面').click('center')

#print json.dumps(poco.agent.hierarchy.dump())

# poco(u'1').click()
# poco(u'乘以').click()
# poco(u'5').click()
# poco(u'等于').click()


# print poco(u'文本编辑器').attr("text")
# print poco(u'文本编辑器').attr("name")
# print poco(u'文本编辑器').attr("type")
# print poco(u'文本编辑器').attr("originType")
# print poco(u'文本编辑器').attr("_instanceId")
# poco(u'文本编辑器').setattr("text","hhh")
# poco.agent.input.keyevent("{F 3}")

time.sleep(1)

