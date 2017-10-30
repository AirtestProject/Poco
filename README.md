# Poco ポコ

**A cross-engine UI automation framework**

[中文README(Chinese README)](README-CN.md)在此。

## Installation

To use `poco` full functionality (Netease internal engine implementations), please install the following modules with scripts given below before installing `poco`.

```sh
# airtest runtime
git clone ssh://git@git-qa.gz.netease.com:32200/gzliuxin/airtest.git
pip install -e airtest

# aircv for airtest
git clone -b open-source ssh://git@git-qa.gz.netease.com:32200/airtest-projects/aircv.git
pip install -e aircv

# hrpc
git clone ssh://git@git-qa.gz.netease.com:32200/maki/hrpc.git
pip install -e hrpc

# hunter-cli
git clone ssh://git@git-qa.gz.netease.com:32200/maki/hunter-cli.git
pip install -e hunter-cli

# hunter lib for airtest
git clone ssh://git@git-qa.gz.netease.com:32200/maki/airtest-hunter.git
pip install -e airtest-hunter
```

Install `poco` and `PocoUnit` for unittest.

```sh
# poco
git clone ssh://git@git-qa.gz.netease.com:32200/maki/poco.git
pip install -e poco

# poco unittest framework
git clone ssh://git@git-qa.gz.netease.com:32200/maki/PocoUnit.git
pip install -e PocoUnit
```


## Basic Concepts

**Target device**: test devices apps or games will run on, usually refers to mobile phones  
**UI proxy**: proxy objects within poco framework, representing 0, 1 or multiple in-game UI elements  
**Node/UI element**: UI element instances within apps/games, namely UI  
**query condition/expression**: a serializable data structure through which poco interacts with **target devices** and selects the corresponding UI elements. Tester usually don't need to pay attention to the internal structure of this expression unless they need to customize the `Selector` class.  

![image](doc/img/hunter-inspector.png)
![image](doc/img/hunter-inspector-text-attribute.png)
![image](doc/img/hunter-inspector-hierarchy-relations.png)

### Definitions of coordinate system and metric space

![image](doc/img/hunter-poco-coordinate-system.png)

#### Normalized Coordinate System

In normalized coordinate system, the height and width of the screen are measured in the range of 1 unit and these two parameters of UI within poco correspond to certain percentage of the screen size. Hence the same UI on devices with different resolution will have same position and size within normalized coordinate system, which is very helpful to write cross-device test cases.

The space of normalized coordinate system is well distributed. By all means, the coordinate of the screen center is (0.5, 0.5) and the computing method of other scalars and vectors are the same as that of Euclidean space.

#### Local Coordinate System（local positioning）

The aim of introducing local coordinate system is to express coordinates with reference to a certain UI. Local coordinate system  takes the top left corner  of UI bounding box as origin, the horizontal rightward as x-axis and the vertical downward as y-axis, with the height and width of the bounding box being 1 unit  and other definitions being similar with normalized  coordinate system.

Local coordinate system is more flexible to be used to locate the position within or out of UI. For instance, the coordinate (0.5, 0.5)corresponds to the center of the UI while coordinates larger than 1 or less than 0 correspond to the position out of the UI.


## Initialization of `poco` Instances

The instantiation methods of poco with various engines are slightly different. This part will take Unity3D as an example. For other engines, please refer to:

* [cocos2dx-js]()
* [android-native]()
* unreal (in development)
* (others see [INTEGRATION guide]() for more details)


```python
from poco.vendor.unity3d import UnityPoco

poco = UnityPoco()
ui = poco('...')
```

## Object Selection and Operation

### Basic Selector

The invocation `poco(...)` instance is to traverse through the render tree structure and select all the UI elements matching given query condition. The first argument is node name and other key word arguments are correspond to other properties of node. For more information, please refer to API Reference.

```python
# select by node name
poco('bg_mission')

# select by name and oyther properties
poco('bg_mission', type='Button')
poco(textMatches='^据点.*$', type='Button', enable=True)
```

![image](doc/img/hunter-poco-select-simple.png)


### Relative Selector

When there is an ambiguity in the objects selected by node names/node types or failing to select objects, try selecting by hierarchy in a corresponding manner

```python
# select by direct child/offspring
poco('main_node').child('list_item').offspring('item')
```

![image](doc/img/hunter-poco-select-relative.png)

### Sequence Selector (index selector, iterator is more recommended for use)

Index and traversal will be performed in default up-down or left-right space orders. If the not-yet-traversed nodes are removed from the screen, an exception will be thrown whereas this is not the case for traversed nodes that are removed. As the traversal order has been determined before in advance, the traversal will be performed in a previous order even though the nodes in views are rearranged during the traversal process.

```python
items = poco('main_node').child('list_item').offspring('item')
print(items[0].child('material_name').get_text())
print(items[1].child('material_name').get_text())
```

![image](doc/img/hunter-poco-select-sequence.png)

### Traverse through a collection of objects

```python
# traverse through every item
items = poco('main_node').child('list_item').offspring('item')
for item in items:
    item.child('icn_item')
```

![image](doc/img/hunter-poco-iteration.png)

### Get object properties

```python
mission_btn = poco('bg_mission')
print(mission_btn.attr('type'))  # 'Button'
print(mission_btn.get_text())  # '据点支援'
print(mission_btn.attr('text'))  # '据点支援' equivalent to .get_text()
print(mission_btn.exists())  # True/False, exists in the screen or not
```

### Object Proxy Related Operation

#### click

The anchorPoint of UI element defaults to the click point. When the first argument is passed to the relative click position, the coordinate of the top-left corner of the bounding box will be `[0, 0]` and the bottom right corner `[1, 1]`. The deviation range can be less than 0 or larger than 1 and if it turns out to be out of 0~1, that means it is beyond the bounding box.

```python
poco('bg_mission').click()
poco('bg_mission').click('center')
poco('bg_mission').click([0.5, 0.5])    # equivalent to center
poco('bg_mission').focus([0.5, 0.5]).click()  # equivalent to above expression
```

![image](doc/img/hunter-poco-click.png)

#### swipe

Take the anchor of UI element as origin and swipe a certain distance towards a direction

```python
joystick = poco('movetouch_panel').child('point_img')
joystick.swipe('up')
joystick.swipe([0.2, -0.2])  # swipe sqrt(0.08) unit distance at 45 degree angle up-and-right
joystick.swipe([0.2, -0.2], duration=0.5)
```

![image](doc/img/hunter-poco-swipe.png)

#### drag
 
Drag to target UI from current UI

```python
poco(text='突破芯片').drag_to(poco(text='岩石司康饼'))
```

![image](doc/img/hunter-poco-drag.png)

#### focus (local positioning)

The origin defaults to anchor when conducting operations related to node coordinates. Therefore click the anchor directly. If local click deviation is needed, focus can be used. Similar with screen coordinate system, focus takes the upper left corner of bounding box as the origin with the length and width measuring 1, the coordinate of the center being `[0.5, 0.5]`, the bottom right corner`[1, 1]`, and so on.

```python
poco('bg_mission').focus('center').click()  # click the center
```


focus can also be used as internal positioning within an objects, as instanced by the example of implementing a scroll operation in ScrollView

```python
scrollView = poco(type='ScollView')
scrollView.focus([0.5, 0.8]).drag_to(scrollView.focus([0.5, 0.2]))
```

#### wait

Wait for the target object to appear and always return  the object itself. If it appears, return it immediately, otherwise, return after timeout

```python
poco('bg_mission').wait(5).click()  # wait 5 seconds at most，click once the object appears
poco('bg_mission').wait(5).exists()  # wait 5 seconds at most，return Exists or Not Exists
```

## Exceptions

```python
from poco.exceptions import PocoTargetTimeout

try:
    poco('guide_panel', type='ImageView').wait_for_appearance()
except PocoTargetTimeout:
    # bugs here as the panel not shown
    raise
```

```python
from poco.exceptions import PocoNoSuchNodeException

img = poco('guide_panel', type='ImageView')
try:
    if not img.exists():
        img.click()
except PocoNoSuchNodeException:
    # If attempt to operate inexistent nodes, an exception will be thrown
    pass
```

# Unit Test

poco is an automation framework. For unit testing, please refer to [PocoUnit](http://git-qa.gz.netease.com/maki/PocoUnit). PocoUnit provides a full set of assertion methods and it is compatible with the unittest in python standard library. 

