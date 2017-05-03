# Poco Flexible Automation Framework (beta)

一个引擎无关的自动化框架。通过HunterRpc进行数据传输，所有接入了[hunter](http://hunter.nie.netease.com)的项目可直接使用该测试框架。

## 安装 (beta version only)

虽然airtest在未来不是必须的，但是目前版本需要安装airtest依赖

```
git clone ssh://git@git-qa.gz.netease.com:32200/gzliuxin/airtest.git
pip install -e airtest

git clone ssh://git@git-qa.gz.netease.com:32200/maki/hunter-cli.git
pip install -e hunter-cli

git clone ssh://git@git-qa.gz.netease.com:32200/maki/airtest-hunter.git
cd airtest-hunter
git checkout dev
cd ..
pip install -e airtest-hunter
```

## 基本概念

![image](http://init.nie.netease.com/images/hunter/inspector/hunter-inspector.png)
![image](http://init.nie.netease.com/images/hunter/inspector/hunter-inspector-text-attribute.png)
![image](http://init.nie.netease.com/images/hunter/inspector/hunter-inspector-hierarchy-search.png)


**对象代理**: 通过poco选择出来代表的游戏内对象  
**对象集合**: 通过poco选择出来代表一组的游戏内对象  
**节点**: 游戏内对象的实例，按照树形结构渲染的每一个对象均表示一个节点  
**选择器**: 使用poco进行选择的表达式，用于限定和匹配目标对象(节点)  

#### 屏幕坐标系

poco所使用的坐标系均为屏幕坐标系，屏幕坐标系定义如下（游戏画面正向）。poco中的对象代理坐标相关的参数或属性会自动换算到屏幕坐标系下，请始终按照屏幕坐标系进行编码。

![image](http://init.nie.netease.com/images/hunter/inspector/screen-coordinate-system.jpg)

## 对象选择与操作

### 选择器实例初始化

```python
from airtest.core.main import set_serialno
from poco.vendor.airtest import AirtestPoco

set_serialno()  # 以airtest的运行框架为例，初始化设备连接
poco = AirtestPoco('g62')  # 传入hunter中的项目代号
```

### 基本选择器

`poco`对象的`__call__`方法就是进行选择，遍历整个渲染树形结构，选出所有满足给定的属性的对象代理。第一个参数为节点名，其余的属性键值对通过命名参数传入。具体可参考API Reference。

```python
# 根据节点名选择
mission_btn = poco('bg_mission')

# 根据属性选择
player_name = poco(text='路人型迪恩', type='Text')
```

### 相对选择器

直接通过节点名或节点类型选择的对象容易产生歧义或无法选择时，可通过相对的方式按层级进行选择

```python
# 直系孩子选择
mission_list = poco('mission_team').child('panel').child('mission_list')

# 后代孩子选择(包括直系)
mission_list = poco('mission_team').offspring('mission_list')

# 兄弟节点选择器
# 例如：选出某功能区入口的menu里的所有Button
function_buttons = poco('entry_node').child('menu_name').sibling(type='Button')
```

### 获取对象代理属性

```python
mission_btn = poco('bg_mission')
print(mission_btn.attr('type'))  # 'Button'
print(mission_btn.get_text())  # '据点支援'
print(mission_btn.attr('text'))  # '据点支援'，与get_text方法等价
print(mission_btn.exists())  # True，表示是否存在界面中
```

### 对象代理操作

**click** 点击对象，默认以anchor对象为点击点

```python
mission_btn = poco('bg_mission')

# 点击这个按钮(以anchor点作为点击点，从图中可看出anchor点在左上角)
mission_btn.click()    

# 点击对象的中心点
mission_btn.click(click_anchor=False) 
```

**swipe** 以对象anchor为起点，朝某个方向滑动一段距离

```python
controller = poco('movetouch_panel').child('point_img')

# 向上滑动一下
controller.swipe('up')

# 朝给定方向滑动(屏幕坐标系)，只管方向，不管距离
controller.swipe([1, -1])

# 朝给定方向移动10%屏幕宽度的距离，并持续0.5s
controller.swipe([1, -1], distance_percent=0.1, duration=0.5)
```

### 遍历对象集合

```python
# 遍历任务列表里的所有任务名
for name in poco('mission_list').offspring('name_text'):
    print(name.get_text())
```

## 断言

...

## 接入参考

1. safaia版本需要高于1.2.0，如果不高于的话项目组master可在[项目](http://hunter.nie.netease.com/mywork/project#/)页直接下载最新版的接入模块。
1. 在项目的`__init__`指令后面插入以下代码片段，然后重启游戏即可

```python
# inspector extension
# 提供hunter终端里的检视器面板
InspectorExt = require('safaia.init.inspect')
InspectorExt.screen = require('safaia.neox.screen')()  # 根据实际情况选择neox/messiah
InspectorExt.ui2d = require('safaia.cocos2dx.utils')   # 目前ui2d选择器只实现了cocosui，其他的ui框架可另外单独实现
Safaia().install(InspectorExt)

# poco automation framework
# 提供poco自动化框架的rpc对象导出
Safaia().install(require('safaia.init.poco'))
```

3. [hunter终端](http://hunter.nie.netease.com) 右上角点击**Inspector**按钮打开检视器面板。


## API Reference

...
