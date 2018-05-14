# coding=utf-8
import xml.etree.ElementTree as ET
from poco import Poco
from poco.agent import PocoAgent
from poco.freezeui.hierarchy import FrozenUIDumper, FrozenUIHierarchy
from poco.utils.airtest import AirtestInput, AirtestScreen
from airtest.core.api import device as current_device
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
        self.size = client.window_size()

    def dumpHierarchy(self):
        xml = self.client.driver.source()
        xml = xml.encode("utf-8")
        data = ios_dump(xml, self.size)
        return data


def ios_dump(xml, screen_size):
    # print(xml)
    root = ET.fromstring(xml)
    data = xml_parser(root, screen_size)
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
    dump = ios_dump(XML, (375, 812))
    pprint(dump)
