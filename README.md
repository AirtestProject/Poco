# Poco Flexible Automation Framework (beta)

一个引擎无关的自动化框架。通过HunterRpc进行数据传输，所有接入了[hunter](http://hunter.nie.netease.com)的项目可直接使用该测试框架。

## 安装 (beta version only)

虽然airtest在未来不是必须的，但是目前版本需要安装airtest依赖

```sh
# airtest runtime
git clone ssh://git@git-qa.gz.netease.com:32200/gzliuxin/airtest.git
pip install -e airtest

# aircv for airtest
git clone -b open-source ssh://git@git-qa.gz.netease.com:32200/airtest-projects/aircv.git
pip install -e aircv

# hunter-cli
git clone ssh://git@git-qa.gz.netease.com:32200/maki/hunter-cli.git
pip install -e hunter-cli

# hunter lib for airtest
git clone -b dev ssh://git@git-qa.gz.netease.com:32200/maki/airtest-hunter.git
pip install -e airtest-hunter

# poco
git clone ssh://git@git-qa.gz.netease.com:32200/maki/poco.git
pip install -e poco
```

## 基本概念

![image](http://init.nie.netease.com/images/hunter/inspector/hunter-inspector.png)
![image](http://init.nie.netease.com/images/hunter/inspector/hunter-inspector-text-attribute.png)
![image](http://init.nie.netease.com/images/hunter/inspector/hunter-inspector-hierarchy-search.png)
![image](http://init.nie.netease.com/images/hunter/inspector/hunter-inspector-hierarchy-relations.png)

**对象代理**: 通过poco选择出来代表的游戏内对象  
**对象集合**: 通过poco选择出来代表一组的游戏内对象  
**节点**: 游戏内对象的实例，按照树形结构渲染的每一个对象均表示一个节点  
**选择器**: 使用poco进行选择的表达式，用于限定和匹配目标对象(节点)  


![image](http://init.nie.netease.com/images/hunter/inspector/hunter-poco-coordinate-system.png)

## 对象选择与操作

### 选择器实例初始化

```python
from airtest.core.main import set_serialno
from poco.vendor.airtest import AirtestPoco

set_serialno()  # 以airtest的运行框架为例，选择连在电脑上的默认设备
poco = AirtestPoco('g62')  # 传入hunter中的项目代号
```

### 基本选择器

`poco`对象的`__call__`方法就是进行选择，遍历整个渲染树形结构，选出所有满足给定的属性的对象代理。第一个参数为节点名，其余的属性键值对通过命名参数传入。具体可参考API Reference。

```python
# 根据节点名选择
poco('bg_mission')

# 节点名和属性选择
poco('bg_mission', type='Button')
poco(text='据点支援', type='Button', enable=True)
```

![image](http://init.nie.netease.com/images/hunter/inspector/hunter-poco-select-simple.png)


### 相对选择器

直接通过节点名或节点类型选择的对象容易产生歧义或无法选择时，可通过相对的方式按层级进行选择

```python
# 直系孩子/后代选择
poco('main_node').child('list_item').offspring('item')
```
``
![image](http://init.nie.netease.com/images/hunter/inspector/hunter-poco-select-relative.png)

### 顺序选择器（索引选择器）

```python
items = poco('main_node').child('list_item').offspring('item')
print(items[0].child('material_name').get_text())
print(items[1].child('material_name').get_text())
```

![image](http://init.nie.netease.com/images/hunter/inspector/hunter-poco-select-sequence.png)

### 获取对象代理属性

```python
mission_btn = poco('bg_mission')
print(mission_btn.attr('type'))  # 'Button'
print(mission_btn.get_text())  # '据点支援'
print(mission_btn.attr('text'))  # '据点支援'，与get_text方法等价
print(mission_btn.exists())  # True，表示是否存在界面中
```

### 对象代理操作

#### click

点击对象，默认以anchor对象为点击点。第一个参数传入点击相对位置，对象包围盒左上角为`[0, 0]`，右下角为`[1, 1]`。

```python
poco('bg_mission').click()
poco('bg_mission').click('center')
poco('bg_mission').click([0.5, 0.5])    # 等价于center
```

![image](http://init.nie.netease.com/images/hunter/inspector/hunter-poco-click.png)

#### swipe

以对象anchor为起点，朝某个方向滑动一段距离

```python
joystick = poco('movetouch_panel').child('point_img')
joystick.swipe('up')
joystick.swipe([0.2, -0.2])
joystick.swipe([0.2, -0.2], duration=0.5)
```

![image](http://init.nie.netease.com/images/hunter/inspector/hunter-poco-swipe.png)

#### drag
 
从当前对象拖拽到目标对象

```python
poco(text='突破芯片').drag_to(poco(text='岩石司康饼'))
```

![image](http://init.nie.netease.com/images/hunter/inspector/hunter-poco-drag.png)

### 遍历对象集合

```python
# 遍历每一个商品
items = poco('main_node').child('list_item').offspring('item')
for item in items:
    item.child('icn_item')
```

![image](http://init.nie.netease.com/images/hunter/inspector/hunter-poco-iteration.png)

## 断言与异常

**基本断言**

```
poco.assert_equal(expr1, expr2, 'message')
poco.assert_greater(…)
```

**捕获异常**

```python
from poco.exceptions import PocoTargetTimeout

try:
    poco('guide_panel', type='ImageView').wait_for_appearance()
except PocoTargetTimeout:
    # 面板没有弹出来，有bug
    raise
```

## 接入参考

1. safaia版本需要高于1.2.0，如果不高于的话项目组master可在[项目](http://hunter.nie.netease.com/mywork/project#/)页直接下载最新版的接入模块。
1. 在项目的`__init__`指令后面插入以下代码片段，然后重启游戏即可

```python

screen_handler = require('safaia.neox.screen')()  # 根据实际情况选择neox/messiah

# screen 扩展，提供屏幕相关的信息和操作
ScreenExtension = require('safaia.init.screen')
ScreenExtension.screen_handler = screen_handler
Safaia().install(ScreenExtension)

# inspector extension
# 提供hunter终端里的检视器面板
InspectorExt = require('safaia.init.inspect')
InspectorExt.screen = screen_handler
InspectorExt.ui2d = require('safaia.cocos2dx.utils')  # 目前ui2d选择器只实现了cocosui，其他的ui框架可另外单独实现
Safaia().install(InspectorExt)

# poco automation framework
# 提供poco自动化框架的rpc对象导出
Safaia().install(require('safaia.init.poco'))
```

3. [hunter终端](http://hunter.nie.netease.com) 右上角点击**Inspector**按钮打开检视器面板。


## API Reference

...
