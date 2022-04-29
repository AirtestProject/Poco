# coding=utf-8
import xml.etree.ElementTree as ET
from poco.pocofw import Poco
from poco.agent import PocoAgent
from poco.freezeui.hierarchy import FrozenUIDumper, FrozenUIHierarchy
from poco.utils.airtest import AirtestInput, AirtestScreen
from poco.utils import six
from airtest.core.api import device as current_device
try:
    from airtest.core.ios.rotation import XYTransformer
except AttributeError:
    raise RuntimeError('The iOS module of Airtest>1.1.7 only supports python3, if you want to use, please upgrade to python3 first.')
from pprint import pprint


class iosPoco(Poco):
    def __init__(self, device=None, **kwargs):
        device = device or current_device()
        if not device or device.__class__.__name__ != 'IOS':
            raise RuntimeError('Please call `connect_device` to connect an iOS device first')

        agent = iosPocoAgent(device)
        super(iosPoco, self).__init__(agent, **kwargs)


class iosPocoAgent(PocoAgent):
    def __init__(self, client):
        self.client = client

        hierarchy = FrozenUIHierarchy(iosDumper(self.client))
        screen = AirtestScreen()
        input = AirtestInput()
        super(iosPocoAgent, self).__init__(hierarchy, input, screen, None)


class iosDumper(FrozenUIDumper):

    def __init__(self, client):
        super(iosDumper, self).__init__()
        self.client = client
        self.size = client.display_info["window_width"], client.display_info["window_height"]

    def dumpHierarchy(self, onlyVisibleNode=True):
        # 当使用了appium/WebDriverAgent时，ipad横屏且在桌面下，坐标需要按照竖屏坐标额外转换一次
        # 判断条件如下：
        # 当ios.using_ios_tagent有值、且为false，说明使用的是appium/WebDriverAgent
        # airtest<=1.2.4时，没有ios.using_ios_tagent的值，说明也是用的appium/wda
        if ((hasattr(self.client, "using_ios_tagent") and not self.client.using_ios_tagent) or
            (not hasattr(self.client, "using_ios_tagent"))) \
                and (self.client.is_pad and self.client.orientation != 'PORTRAIT' and self.client.home_interface()):
            switch_flag = True
        else:
            switch_flag = False
        jsonObj = self.client.driver.source(format='json')
        w, h = self.size
        if self.client.orientation in ['LANDSCAPE', 'UIA_DEVICE_ORIENTATION_LANDSCAPERIGHT']:
            w, h = h, w
        data = json_parser(jsonObj, (w, h), switch_flag=switch_flag, ori=self.client.orientation)
        return data

    def dumpHierarchy_xml(self):
        xml = self.client.driver.source()
        xml = xml.encode("utf-8")
        data = ios_dump_xml(xml, self.size)
        return data


def ios_dump_xml(xml, screen_size):
    root = ET.fromstring(xml)
    data = xml_parser(root, screen_size)
    return data


def json_parser(node, screen_size, switch_flag=False, ori='PORTRAIT'):
    """

    :param node: node info {}
    :param screen_size: ios.windows_size()
    :param switch_flag: If it is an ipad , when on the desktop, all coordinates must be converted to vertical screen coordinates
    :param ori: wda ['PORTRAIT', 'LANDSCAPE',
                    'UIA_DEVICE_ORIENTATION_LANDSCAPERIGHT',
                    'UIA_DEVICE_ORIENTATION_PORTRAIT_UPSIDEDOWN']
    :return:
    """
    screen_w, screen_h = screen_size

    if "name" in node and node["name"]:
        name = node["name"]
    else:
        name = node["type"]

    data = {
        "name": name,
        "payload": {}
    }

    if six.PY2:
        for key in [x for x in node.keys() if x not in ['frame', 'children']]:
            data["payload"][key.encode("utf-8")] = node[key]
    else:
        for key in [x for x in node.keys() if x not in ['frame', 'children']]:
            data["payload"][key] = node[key]

    w = float(node["rect"]["width"])
    h = float(node["rect"]["height"])
    x = float(node["rect"]["x"])
    y = float(node["rect"]["y"])

    if switch_flag:
        x, y = XYTransformer.ori_2_up(
            (x, y),
            (screen_w, screen_h),
            ori
        )
    if switch_flag and ori == 'LANDSCAPE':
        w, h = h, w
        data["payload"]["pos"] = [
            (x + w / 2) / screen_w,
            (y - h / 2) / screen_h
        ]
    elif switch_flag and ori == 'UIA_DEVICE_ORIENTATION_LANDSCAPERIGHT':
        w, h = h, w
        data["payload"]["pos"] = [
            (x - w / 2) / screen_w,
            (y + h / 2) / screen_h
        ]
    elif switch_flag and ori == 'UIA_DEVICE_ORIENTATION_PORTRAIT_UPSIDEDOWN':
        data["payload"]["pos"] = [
            (x - w / 2) / screen_w,
            (y - h / 2) / screen_h
        ]
    else:
        data["payload"]["pos"] = [
            (x + w / 2) / screen_w,
            (y + h / 2) / screen_h
        ]

    data["payload"]["name"] = name
    data["payload"]["size"] = [w / screen_w, h / screen_h]
    
    data["payload"]["zOrders"] = {
        "local": 0,
        "global": 0,
    }
    data["payload"]["anchorPoint"] = [0.5, 0.5]

    # TODO: w = 0 and h = 0 situation need to solve with
    # roll back set as True when finding a visible child
    if "visible" not in node:
        if (x >= 0 or x + w > 0) and (x < screen_w) and (y >= 0 or y + h > 0) and (y < screen_h):
            data["payload"]["visible"] = True
        elif w == 0 or h == 0:
            data["payload"]["visible"] = True
        else:
            data["payload"]["visible"] = False

    children_data = []
    if "children" in node:
        for child in node["children"]:
            child_data = json_parser(child, screen_size=screen_size, switch_flag=switch_flag, ori=ori)
            children_data.append(child_data)

    if children_data:
        data["children"] = children_data
        if data["payload"]["visible"] is False:
            for child_node in children_data:
                if child_node["payload"].get("visible") is True:
                    data["payload"]["visible"] = True
                    break

    return data


def xml_parser(node, screen_size):
    # print(node)
    # print(node.attrib)
    screen_w, screen_h = screen_size

    name = node.attrib.get("name", node.tag)
    data = {
        "name": name,
        "payload": node.attrib,
    }

    w = float(node.attrib["width"])
    h = float(node.attrib["height"])
    x = float(node.attrib["x"])
    y = float(node.attrib["y"])

    data["payload"]["name"] = name
    data["payload"]["size"] = [w / screen_w, h / screen_h]
    data["payload"]["pos"] = [
        (x + w / 2) / screen_w,
        (y + h / 2) / screen_h
    ]
    data["payload"]["zOrders"] = {
        "local": 0,
        "global": 0,
    }
    data["payload"]["anchorPoint"] = (0.5, 0.5)

    children_data = []
    for child in node:
        child_data = xml_parser(child, screen_size)
        children_data.append(child_data)

    if children_data:
        data["children"] = children_data

    return data


if __name__ == '__main__':
    XML = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<XCUIElementTypeApplication type=\"XCUIElementTypeApplication\" name=\"健康\" label=\"健康\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n  <XCUIElementTypeWindow type=\"XCUIElementTypeWindow\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n    <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n      <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n        <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n          <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n            <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n              <XCUIElementTypeNavigationBar type=\"XCUIElementTypeNavigationBar\" name=\"WDTodayDayPageView\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"44\" width=\"375\" height=\"44\">\n                <XCUIElementTypeButton type=\"XCUIElementTypeButton\" name=\"五月\" label=\"五月\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"44\" width=\"65\" height=\"44\"/>\n                <XCUIElementTypeButton type=\"XCUIElementTypeButton\" name=\"查看个人资料\" label=\"查看个人资料\" enabled=\"true\" visible=\"true\" x=\"334\" y=\"53\" width=\"25\" height=\"26\"/>\n              </XCUIElementTypeNavigationBar>\n              <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n                <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n                  <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n                    <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n                      <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n                        <XCUIElementTypeTable type=\"XCUIElementTypeTable\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n                          <XCUIElementTypeOther type=\"XCUIElementTypeOther\" name=\"健身记录\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"176\" width=\"375\" height=\"37\">\n                            <XCUIElementTypeOther type=\"XCUIElementTypeOther\" name=\"健身记录\" label=\"健身记录\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"176\" width=\"375\" height=\"37\"/>\n                          </XCUIElementTypeOther>\n                          <XCUIElementTypeCell type=\"XCUIElementTypeCell\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"213\" width=\"375\" height=\"82\">\n                            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"1.8￼公里\" name=\"1.8￼公里\" label=\"1.8￼公里\" enabled=\"true\" visible=\"true\" x=\"254\" y=\"214\" width=\"93\" height=\"54\"/>\n                            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"今天 上午10:05\" name=\"今天 上午10:05\" label=\"今天 上午10:05\" enabled=\"true\" visible=\"true\" x=\"262\" y=\"266\" width=\"86\" height=\"15\"/>\n                            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"步行 + 跑步距离\" name=\"步行 + 跑步距离\" label=\"步行 + 跑步距离\" enabled=\"true\" visible=\"true\" x=\"28\" y=\"220\" width=\"124\" height=\"21\"/>\n                          </XCUIElementTypeCell>\n                          <XCUIElementTypeCell type=\"XCUIElementTypeCell\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"295\" width=\"375\" height=\"82\">\n                            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"2,438￼步\" name=\"2,438￼步\" label=\"2,438￼步\" enabled=\"true\" visible=\"true\" x=\"209\" y=\"296\" width=\"138\" height=\"54\"/>\n                            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"今天 上午10:05\" name=\"今天 上午10:05\" label=\"今天 上午10:05\" enabled=\"true\" visible=\"true\" x=\"262\" y=\"348\" width=\"86\" height=\"15\"/>\n                            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"步数\" name=\"步数\" label=\"步数\" enabled=\"true\" visible=\"true\" x=\"28\" y=\"302\" width=\"35\" height=\"21\"/>\n                          </XCUIElementTypeCell>\n                          <XCUIElementTypeCell type=\"XCUIElementTypeCell\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"377\" width=\"375\" height=\"82\">\n                            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"今天 上午9:24\" name=\"今天 上午9:24\" label=\"今天 上午9:24\" enabled=\"true\" visible=\"true\" x=\"268\" y=\"430\" width=\"79\" height=\"15\"/>\n                            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"4￼层\" name=\"4￼层\" label=\"4￼层\" enabled=\"true\" visible=\"true\" x=\"300\" y=\"378\" width=\"48\" height=\"54\"/>\n                            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"已爬楼层\" name=\"已爬楼层\" label=\"已爬楼层\" enabled=\"true\" visible=\"true\" x=\"28\" y=\"384\" width=\"70\" height=\"21\"/>\n                          </XCUIElementTypeCell>\n                        </XCUIElementTypeTable>\n                      </XCUIElementTypeOther>\n                    </XCUIElementTypeOther>\n                  </XCUIElementTypeOther>\n                </XCUIElementTypeOther>\n              </XCUIElementTypeOther>\n              <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n                <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"88\" width=\"375\" height=\"88\">\n                  <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"88\" width=\"375\" height=\"88\">\n                    <XCUIElementTypeScrollView type=\"XCUIElementTypeScrollView\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"105\" width=\"375\" height=\"35\">\n                      <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"105\" width=\"375\" height=\"58\">\n                        <XCUIElementTypeOther type=\"XCUIElementTypeOther\" name=\"5月13日 星期日\" label=\"5月13日 星期日\" enabled=\"true\" visible=\"true\" x=\"13\" y=\"110\" width=\"36\" height=\"35\"/>\n                        <XCUIElementTypeOther type=\"XCUIElementTypeOther\" name=\"今天, 5月14日 星期一\" label=\"今天, 5月14日 星期一\" enabled=\"true\" visible=\"true\" x=\"65\" y=\"110\" width=\"36\" height=\"35\"/>\n                        <XCUIElementTypeOther type=\"XCUIElementTypeOther\" name=\"5月15日 星期二\" label=\"5月15日 星期二\" enabled=\"true\" visible=\"true\" x=\"118\" y=\"110\" width=\"35\" height=\"35\"/>\n                        <XCUIElementTypeOther type=\"XCUIElementTypeOther\" name=\"5月16日 星期三\" label=\"5月16日 星期三\" enabled=\"true\" visible=\"true\" x=\"170\" y=\"110\" width=\"35\" height=\"35\"/>\n                        <XCUIElementTypeOther type=\"XCUIElementTypeOther\" name=\"5月17日 星期四\" label=\"5月17日 星期四\" enabled=\"true\" visible=\"true\" x=\"222\" y=\"110\" width=\"35\" height=\"35\"/>\n                        <XCUIElementTypeOther type=\"XCUIElementTypeOther\" name=\"5月18日 星期五\" label=\"5月18日 星期五\" enabled=\"true\" visible=\"true\" x=\"274\" y=\"110\" width=\"36\" height=\"35\"/>\n                        <XCUIElementTypeOther type=\"XCUIElementTypeOther\" name=\"5月19日 星期六\" label=\"5月19日 星期六\" enabled=\"true\" visible=\"true\" x=\"326\" y=\"110\" width=\"36\" height=\"35\"/>\n                      </XCUIElementTypeOther>\n                    </XCUIElementTypeScrollView>\n                    <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"2018年5月14日 星期一\" name=\"2018年5月14日 星期一\" label=\"2018年5月14日 星期一\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"148\" width=\"375\" height=\"20\"/>\n                  </XCUIElementTypeOther>\n                </XCUIElementTypeOther>\n              </XCUIElementTypeOther>\n            </XCUIElementTypeOther>\n          </XCUIElementTypeOther>\n        </XCUIElementTypeOther>\n      </XCUIElementTypeOther>\n      <XCUIElementTypeTabBar type=\"XCUIElementTypeTabBar\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"729\" width=\"375\" height=\"83\">\n        <XCUIElementTypeButton type=\"XCUIElementTypeButton\" value=\"1\" name=\"今天\" label=\"今天\" enabled=\"true\" visible=\"true\" x=\"2\" y=\"730\" width=\"90\" height=\"48\"/>\n        <XCUIElementTypeButton type=\"XCUIElementTypeButton\" name=\"健康数据\" label=\"健康数据\" enabled=\"true\" visible=\"true\" x=\"96\" y=\"730\" width=\"90\" height=\"48\"/>\n        <XCUIElementTypeButton type=\"XCUIElementTypeButton\" name=\"数据来源\" label=\"数据来源\" enabled=\"true\" visible=\"true\" x=\"190\" y=\"730\" width=\"89\" height=\"48\"/>\n        <XCUIElementTypeButton type=\"XCUIElementTypeButton\" name=\"医疗急救卡\" label=\"医疗急救卡\" enabled=\"true\" visible=\"true\" x=\"283\" y=\"730\" width=\"90\" height=\"48\"/>\n      </XCUIElementTypeTabBar>\n    </XCUIElementTypeOther>\n  </XCUIElementTypeWindow>\n  <XCUIElementTypeWindow type=\"XCUIElementTypeWindow\" enabled=\"true\" visible=\"false\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n    <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"false\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n      <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"false\" x=\"0\" y=\"812\" width=\"375\" height=\"233\"/>\n    </XCUIElementTypeOther>\n  </XCUIElementTypeWindow>\n  <XCUIElementTypeWindow type=\"XCUIElementTypeWindow\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"812\">\n    <XCUIElementTypeStatusBar type=\"XCUIElementTypeStatusBar\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"44\">\n      <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"44\">\n        <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"0\" y=\"0\" width=\"375\" height=\"44\">\n          <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"14\" y=\"0\" width=\"172\" height=\"29\"/>\n          <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"true\" x=\"190\" y=\"0\" width=\"171\" height=\"29\"/>\n          <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"false\" x=\"14\" y=\"10\" width=\"68\" height=\"19\">\n            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"10:56\" name=\"10:56\" label=\"10:56\" enabled=\"true\" visible=\"false\" x=\"27\" y=\"14\" width=\"42\" height=\"18\"/>\n          </XCUIElementTypeOther>\n          <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"false\" x=\"21\" y=\"8\" width=\"56\" height=\"22\"/>\n          <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"false\" x=\"293\" y=\"10\" width=\"68\" height=\"19\">\n            <XCUIElementTypeOther type=\"XCUIElementTypeOther\" name=\"信号强度：4（共 4 格）\" label=\"信号强度：4（共 4 格）\" enabled=\"true\" visible=\"false\" x=\"293\" y=\"17\" width=\"18\" height=\"12\"/>\n            <XCUIElementTypeStaticText type=\"XCUIElementTypeStaticText\" value=\"4G\" name=\"4G\" label=\"4G\" enabled=\"true\" visible=\"false\" x=\"315\" y=\"16\" width=\"17\" height=\"15\"/>\n            <XCUIElementTypeOther type=\"XCUIElementTypeOther\" value=\"正在充电\" name=\"电池电量：68%\" label=\"电池电量：68%\" enabled=\"true\" visible=\"false\" x=\"336\" y=\"17\" width=\"25\" height=\"12\"/>\n          </XCUIElementTypeOther>\n          <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"false\" x=\"293\" y=\"10\" width=\"68\" height=\"19\"/>\n        </XCUIElementTypeOther>\n        <XCUIElementTypeOther type=\"XCUIElementTypeOther\" enabled=\"true\" visible=\"false\" x=\"8\" y=\"24\" width=\"82\" height=\"14\"/>\n      </XCUIElementTypeOther>\n    </XCUIElementTypeStatusBar>\n  </XCUIElementTypeWindow>\n</XCUIElementTypeApplication>\n"

    import json
    import requests
    jsonStr = requests.get("http://10.254.51.239:8100/source?format=json")
    jsonStr = jsonStr.text

    jsonObj = json.loads(jsonStr)

    dump = ios_dump_xml(XML, (375, 812))

    dumpJson = ios_dump_json(jsonObj["value"], (375, 812))
    pprint(dumpJson)
