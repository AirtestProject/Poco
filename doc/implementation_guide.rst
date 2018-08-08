
Implementation Guide
====================

This guide helps you implement and integrate poco-sdk with your game/app step by step.

Poco-sdk now supports following languages:

- python
- js
- lua
- c#
- java

More language will come in future.

Getting Poco SDK
----------------

First clone the `poco-sdk repo`_. Each languages are located in ``poco-sdk/sdk/*`` separately.

.. code-block:: bash

    git clone https://github.com/AirtestProject/Poco-SDK.git

You can just copy the source code of corresponding language to your project script folder.

Implement the Abstract Method
-----------------------------

In your SDK, you need to implement several important functions to drive the entire SDK.

Dump
....

This function must be implemented. But, it is very simple to implement. The onlyVisibleNode argument is not required, but must receive an argument.

.. code-block:: python

    def Dump(onlyVisibleNode):
        return YourDumper().dumpHierarchy(onlyVisibleNode)

    # or like this
    def Dump(_):
        return YourDumper().dumpHierarchy()


Screenshot
..........

If needed, can implement this function so that it can be called correctly in Poco. The return is a string of base64 encrypted strings and its format.

.. code-block:: python

    def Screenshot(self, width):
        return [base64.b64encode(YourAPI.GetScreenshot(width)), "bmp"]


Click, Swipe, LongClick
.......................

These functions are also required to make all of Poco's features work.

.. Warning::
    Note that the form of the argument passed in is a percentage.If your API does not support this form of input, calculate the correct coordinates yourself.Just Like this ``x = Left + Width * x``, ``y = Top + Height * y``


.. code-block:: python

    def Click(self, x, y):
        # x = Left + Width * x
        # y = Top + Height * y
        YourAPI.Click(x, y)

    def Swipe(self, x1, y1, x2, y2, duration):
        YourAPI.Swipe(x1, y1, x2, y2, duration)

    def LongClick(self, x, y, duration):
        YourAPI.LongClick(x1, y1, x2, y2, duration)


.. note::

    Other optional functions are ``GetScreenSize``, ``GetSDKVersion``, and if your Poco driver needs other functions, you can add it yourself.


Initialize poco-sdk after game launched
.......................................

A variety of basic functions have been implemented, and the final step is to establish communication between the client and the server. Poco offers a simple RPC service, you can use it like below.

.. code-block:: python

    from poco.sdk.std.rpc.controller import StdRpcEndpointController
    from poco.sdk.std.rpc.reactor import StdRpcReactor
    from poco.utils.net.transport.tcp import TcpSocket

    reactor = StdRpcReactor()
    reactor.register('Dump', Dump)
    reactor.register('Screenshot', Screenshot)
    reactor.register('Click', Click)
    reactor.register('Swipe', Swipe)
    reactor.register('LongClick', LongClick)
    # If you have implemented other functions, don't forget to register it.

    transport = TcpSocket()
    transport.bind(("localhost", 15004))  # Listening to a port
    rpc = StdRpcEndpointController(transport, reactor)
    rpc.serve_forever()  # Enable RPC listening service and listen for messages sent by the client.

.. note::

    You can use other RPC frameworks, but I would recommend using our Poco RPC framework.


Abstract Class/Interface Implementation
........................................

To implement your own version of poco sdk, you only need to implement the following 2 classes/interfaces and override its abstract method. This section shows the details about implementing the abstract method in classes or interfaces.

.. code-block:: python

    class YourNode(AbstractNode):   
        def __init__(self, yourElement):
            self.Element = yourElement

        def getParent(self):
            pass

        def getChildren(self):
            pass

        def getAttr(self, attrName):
            pass

        def setAttr(self, attrName, val):
            pass

        # Can override this function if needed
        def getAvailableAttributeNames(self):
            pass

    class YourDumper(AbstractDumper):

        def __init__(self, root):
            pass

        def getRoot(self):
            pass
    
    


:py:class:`AbstractNode <poco.sdk.AbstractNode>`
------------------------------------------------

4 methods should be override

getParent
.........

This function returns the parent of a node, so it is very simple to overwrite. According to your own API function, return a parent node.

.. code-block:: python

    def getParent(self):
        return YourNode(self.YourElement.GetParentElement)

getChildren
...........

This function returns an iterator of all child nodes of a node. It's also very simple to implement, you can write a code similar to the following

.. code-block:: python

    def getChildren(self):
        Children = self.Element.GetChildren()
        for node in Children:
            yield YoueNode(node)

getAttr
.......

This function role is to return a property value of the node. So you have to return the corresponding property value based on the given argument.

.. code-block:: python

    def getAttr(self, attrName):

        if attrName == 'name':
            return  self.Element.GetName()

        if attrName == 'type':
            return self.Element.GetType()

        if attrName == 'pos':
            return self.Element.GetPos()
            
        return super(YourNode, self).getAttr(attrName)

.. Warning::

    The attributes of ``anchor``, ``pos``, and ``size`` are well defined, and you must return a value in the specified format. For more information, please read the comments in :py:class:`AbstractNode <poco.sdk.AbstractNode>`.

setAttr
.......

The purpose of this function is to set an attribute. You can override this function as needed. Sometimes not all properties can be set. At this point you can throw the error appropriately.

.. code-block:: python

    def setAttr(self, attrName, val):

        if attrName == 'text':
            self.Element.SetText(val)

        if attrName == 'name':
            self.Element.SetName(val)

        raise UnableToSetAttributeException(attrName, self)


getAvailableAttributeNames
..........................

This function is optional. If your API provides more property access, you can override this function and add other properties.

.. code-block:: python

    def getAvailableAttributeNames(self):
        return super(YourNode, self).getAvailableAttributeNames() + ('yourNewattr1', 'yourNewattr2')



:py:class:`AbstractDumper <poco.sdk.AbstractDumper>`
-----------------------------------------------------

1 method should be override

getRoot
.......

You only need to override this function. This function is also very simple to implement, just return the root surface of the device. So, Poco can access the properties of all child elements through this root surface and your overloaded functhons ``getChildren``, ``getAttr``.

.. code-block:: python

    def getRoot(self):
        return YourNode(YourAPI.GetRootElement())




.. _poco-sdk repo: https://github.com/AirtestProject/Poco-SDK
