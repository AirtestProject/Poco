# coding=utf-8

__author__ = 'lxn3032'
__all__ = ['IDumper', 'AbstractDumper']


class IDumper(object):
    """
    This interface defines standard dumper behavior. Dumper is only introduced to get the hierarchy information and
    convert it into serializable data.
    """

    def getRoot(self):
        """
        Return the root node of the UI Hierarchy. The node's information is wrapped by 
        :py:class:`AbstractNode <poco.sdk.AbstractNode>`.
        See definition of :py:class:`AbstractNode <poco.sdk.AbstractNode>` for more details.

        Returns:
            :py:class:`inherit from AbstractNode <poco.sdk.AbstractNode>`: An instance holds the hierarchy data.
        """

        raise NotImplementedError

    def dumpHierarchy(self):
        """
        Return a dict holding the hierarchy data and its structure should be as follows. The dict should be json 
        serializable.

        Structure of the dict::

            {
                'name': '<a recognizable string, can be duplicated or just leave by default if cannot determine. meaningful is better.>'
                
                # All available attributes of this node in form of key-value pairs.
                'payload': {
                    'name': '',
                    'pos': [0, 0],
                    'size': [1, 1],
                    ...
                },
                
                # If no child, do not assign this entry.
                'children': [
                    {...},  # Same structure as this dict. 
                ],
            }

        Returns:
            :obj:`dict` or :obj:`NoneType`: Hierarchy data or None
        """

        raise NotImplementedError


class AbstractDumper(IDumper):
    """
    This class partially implements ``IDumper`` using general traversal algorithm. To dump the hierarchy from a root 
    node, this dumper retrieves all available attributes of this root node and list all its children. Then apply the 
    same procedure on each child (treat each child as root node) until a node which has no child.
    """

    def dumpHierarchy(self):
        """
        Returns:
            :obj:`dict`: A json serializable dict holds the whole hierarchy data.
        """

        return self.dumpHierarchyImpl(self.getRoot())

    def dumpHierarchyImpl(self, node):
        """
        Crawl the hierarchy tree using the simple BFS algorithm. ``dump`` is engine independent as the hierarchy 
        structure is wrapped by :py:class:`AbstractNode <poco.sdk.AbstractNode>`, so ``dump`` can be algorithmized. 
        Here shows the simplest implementation by default. If you like, you can implement your own algorithm to optimize 
        the speed.

        .. note:: Do not call this method in explicitly as this is an internal impl function, call \
         :py:meth:`dumpHierarchy() <poco.sdk.AbstractDumper.AbstractDumper.dumpHierarchy>` if you want to dump a 
         hierarchy.

        Args:
            node: Root node of the hierarchy to be dumped.

        Returns:
            :obj:`dict`: A json serializable dict holds the whole hierarchy data.
        """

        if not node:
            return None

        payload = {}
        for attrName, attrVal in node.enumerateAttrs():
            if attrVal is not None:
                payload[attrName] = attrVal

        result = {}
        children = []
        for child in node.getChildren():
            if child.getAttr('visible'):
                children.append(self.dumpHierarchyImpl(child))
        if len(children) > 0:
            result['children'] = children

        result['name'] = node.getAttr('name')
        result['payload'] = payload

        return result
