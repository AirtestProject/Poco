# coding=utf-8


class HierarchyInterface(object):
    """
    This is one of the main communication interfaces. This interface defines hierarchy-related behaviours assembling 
    from `poco.sdk.AbstractDumper.IDumper`, `poco.sdk.Attributor` and `poco.sdk.Selector`. The hierarchy mentioned is 
    the real hierarchy on target app runtime, e.g. a game's UI hierarchy in its runtime.  
    """

    def select(self, query, multiple):
        """
        Select UI elements matches given query condition and return a list containing the selection.

        :param query: Query condition (query expression). Structure specification refers to `poco.sdk.Selector`.
        :param multiple: Whether or not to select element multiple. This method returns once a node found if multiple
            is True, returns after traversing through all nodes otherwise.
        :return: A list of UI elements.
        """

        raise NotImplementedError

    def dump(self):
        """
        Get the UI hierarchy with it origin structure and attributes, then store into a json serializable dict.

        :return: A dict represents the hierarchy structure. Structure specification refers to 
            `poco.sdk.AbstractDumper.IDumper`.
        """

        raise NotImplementedError

    def getAttr(self, nodes, name):
        """
        Get attribute of UI element.

        :param nodes: UI element or list of UI elements. Only the first UI element will be used if a list of UI elements 
            given.
        :param name: The attribute name in string.
        """

        raise NotImplementedError

    def setAttr(self, nodes, name, value):
        """
        Set attribute of UI element.

        :param nodes: UI element or list of UI elements. Only the first UI element will be used if a list of UI elements 
            given.
        :param name: The attribute name in string.
        :param value: New value to be set.
        """

        raise NotImplementedError
