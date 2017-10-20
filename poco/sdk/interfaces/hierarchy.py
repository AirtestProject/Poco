# coding=utf-8


class HierarchyInterface(object):
    """
    This is one of the main communication interfaces. This interface defines hierarchy-related behaviours assembling 
    from :py:class:`IDumper <poco.sdk.AbstractDumper.IDumper>`, :py:class:`Attributor <poco.sdk.Attributor>` and 
    :py:class:`Selector <poco.sdk.Selector>`. The hierarchy mentioned is the real hierarchy on target app runtime.
    e.g. a game's UI hierarchy in its runtime. 
    """

    def select(self, query, multiple):
        """
        Select UI elements matches given query condition and return a list containing the selection.

        Args:
            query (:obj:`tuple`): Query condition (query expression). Structure specification refers to 
             :py:class:`Selector <poco.sdk.Selector>`.
            multiple (:obj:`bool`): Whether or not to select element multiple. This method returns once a node found if 
             multiple is True, returns after traversing through all nodes otherwise.

        Returns:
            :obj:`list` : A list of UI elements.
        """

        raise NotImplementedError

    def dump(self):
        """
        Get the UI hierarchy with its origin structure and attributes, then store into a json serializable dict.

        Returns:
            :obj:`dict` : A dict represent the hierarchy structure. Structure specification refers to \
             :py:class:`IDumper <poco.sdk.AbstractDumper.IDumper>`.
        """

        raise NotImplementedError

    def getAttr(self, nodes, name):
        """
        Get attribute of UI element.

        Args:
            nodes: UI element or list of UI elements. Only the first UI element will be used if a list of UI elements 
             given.
            name (:obj:`str`): The attribute name in string.
        """

        raise NotImplementedError

    def setAttr(self, nodes, name, value):
        """
        Set attribute of UI element.

        Args:
            nodes: UI element or list of UI elements. Only the first UI element will be used if a list of UI elements 
             given.
            name (:obj:`str`): The attribute name in string.
            value: New value to be set.

        Raises:
            UnableToSetAttributeException: If fail to set attributes on given UI element or your engine dose not support 
             mutating attributes or you are not going to allow tester to change the attribute in test scripts, you can 
             raise this exception at the implementation.
        """

        raise NotImplementedError
