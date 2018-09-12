# coding=utf-8

__author__ = 'lxn3032'
__all__ = ['IDumper', 'AbstractDumper']


class IDumper(object):
    """
    This interface defines the standard dumper behavior. Dumper class is introduced to get the hierarchy information and
    convert it into serializable data.
    """

    def getRoot(self):
        """
        Return the root node of the UI Hierarchy. The node information is wrapped by
        :py:class:`AbstractNode <poco.sdk.AbstractNode>`.
        See definition of :py:class:`AbstractNode <poco.sdk.AbstractNode>` for more details.

        Returns:
            :py:class:`inherit from AbstractNode <poco.sdk.AbstractNode>`: instance that holds the hierarchy data
        """

        raise NotImplementedError

    def dumpHierarchy(self, onlyVisibleNode):
        """
        Return the json serializable dictionary holding the hierarchy data. Refer to sample of returned structure object
        below.

        Structure of the dict::

            {
                # name can be duplicated from the original name or just left the default one
                # if it cannot be determined, however providing some meaningful name is preferred
                'name': '<a recognizable string>'
                
                # All available attributes of this node are in form of key-value pairs
                'payload': {
                    'name': '',
                    'pos': [0, 0],
                    'size': [1, 1],
                    ...
                },
                
                # If there is no child, this part can be omitted
                'children': [
                    {...},  # Same structure as this dict. 
                ],
            }

        Returns:
            :obj:`dict` or :obj:`NoneType`: hierarchy data or None
        """

        raise NotImplementedError


class AbstractDumper(IDumper):
    """
    This class partially implements ``IDumper`` using general traversal algorithm. In order to dump the hierarchy from
    the root node, this dumper first retrieves all available attributes of the root node and also the list all its
    children and then applies the same procedures as described on each child (i.e. treats each child as a root node)
    until the node that has no child(ren) is reached.
    """

    def dumpHierarchy(self, onlyVisibleNode=True):
        """
        Returns:
            :obj:`dict`: json serializable dict holding the whole hierarchy data
        """

        return self.dumpHierarchyImpl(self.getRoot(), onlyVisibleNode)

    def dumpHierarchyImpl(self, node, onlyVisibleNode=True):
        """
        Crawl the hierarchy tree using the simple DFS algorithm. The ``dump`` procedure is the engine independent as
        the hierarchy structure is wrapped by :py:class:`AbstractNode <poco.sdk.AbstractNode>` and therefore the
        ``dump`` procedure can be algorithmized.

        Following code demonstrates the simplest implementation. Feel free to implement your own algorithms to
        optimize the performance.

        .. note:: Do not explicitly call this method as this is an internal function, call
                  :py:meth:`dumpHierarchy() <poco.sdk.AbstractDumper.AbstractDumper.dumpHierarchy>` function instead
                  if you want to dump the hierarchy.

        Args:
            node(:py:class:`inherit from AbstractNode <poco.sdk.AbstractNode>`): root node of the hierarchy to be
             dumped
            onlyVisibleNode(:obj:`bool`): dump only the visible nodes or all nodes, default to True

        Returns:
            :obj:`dict`: json serializable dict holding the whole hierarchy data
        """

        if not node:
            return None

        payload = {}

        # filter out all None values
        for attrName, attrVal in node.enumerateAttrs():
            if attrVal is not None:
                payload[attrName] = attrVal

        result = {}
        children = []
        for child in node.getChildren():
            if not onlyVisibleNode or child.getAttr('visible'):
                children.append(self.dumpHierarchyImpl(child, onlyVisibleNode))
        if len(children) > 0:
            result['children'] = children

        result['name'] = payload.get('name') or node.getAttr('name')
        result['payload'] = payload

        return result
