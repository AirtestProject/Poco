# coding=utf-8


class HierarchyInterface(object):
    """
    This is one of the main communication interfaces. This interface defines hierarchy-related behaviour assembling
    from :py:class:`IDumper <poco.sdk.AbstractDumper.IDumper>`, :py:class:`Attributor <poco.sdk.Attributor>` and 
    :py:class:`Selector <poco.sdk.Selector>`. The hierarchy mentioned is the real hierarchy on target app runtime,
    e.g. a game UI hierarchy in its runtime.
    """

    def select(self, query, multiple):
        """
        Select UI element(s) matching the given query expression and return the list of selected UI element(s)

        Args:
            query (:obj:`tuple`): query expression,  for the structure specification refer to
             :py:class:`Selector <poco.sdk.Selector>`.
            multiple (:obj:`bool`): whether or not to select multiple elements,  if False, the method terminates \
            immediately once the node is found, otherwise the method travers through all nodes and then terminates

        Returns:
            :obj:`list` : list of UI elements corresponding to the given query expression
        """

        raise NotImplementedError

    def dump(self):
        """
        Get the UI hierarchy with its origin structure and attributes, then store the structure and attributes  into
        a json serializable dictionary.

        Returns:
            :obj:`dict` : dict representing the hierarchy structure. Structure specification refers to \
             :py:class:`IDumper <poco.sdk.AbstractDumper.IDumper>`.
        """

        raise NotImplementedError

    def getAttr(self, nodes, name):
        """
        Get attribute of UI element.

        Args:
            nodes: UI element or list of UI elements, if there is a list of UI elements provided, then only the \
            first UI element will be used
            name (:obj:`str`): attribute name
        """

        raise NotImplementedError

    def setAttr(self, nodes, name, value):
        """
        Set attribute of UI element.

        Args:
            nodes: UI element or list of UI elements, if there is a list of UI elements provided, then only the \
            first UI element will be used
            name (:obj:`str`): attribute name
            value: new value to be set.

        Raises:
            UnableToSetAttributeException: raised when：

                * fails to set attributes on given UI element
                * the  engine does not support mutating attributes
                * developer does not allow to change the attribute value by implementation
        """

        raise NotImplementedError
