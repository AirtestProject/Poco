# coding=utf-8

__author__ = 'lxn3032'
__all__ = ['AbstractDumper']


class IDumper(object):
    """
    This interface defines standard dumper behavior. Dumper is only introduced to get the hierarchy information and
    convert it into serializable data.
    """

    def getRoot(self):
        """
        Return the root node of the UI Hierarchy. The node's information is wrapped by `support.poco.sdk.AbstractNode`.
        See definition of `AbstractNode` for more details.

        :rettype: instance or instance inherit from `support.poco.sdk.AbstractNode`
        """

        raise NotImplementedError

    def dumpHierarchy(self):
        """
        Return a dict holding the hierarchy data and its structure should be as follows. The dict should be json 
        serializable.
        ```py
        {
            'name': '<a recognizable string, can be duplicated. meaningful is better.>'
            
            # All available attributes of this node in the form of key-value pairs.
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
        ```

        :rettype: `dict` holds the hierarchy data or NoneType
        """

        raise NotImplementedError


class AbstractDumper(IDumper):
    """
    This class partially implements `IDumper` using general traversal algorithm. To dump the hierarchy from a root node, 
    this dumper retrieves all available attributes of this root node and list all its children. Then apply the same 
    procedure on each child (treat each child as root node) until a node which has no child.
    """

    def dumpHierarchy(self):
        return self.dumpHierarchyImpl(self.getRoot())

    def dumpHierarchyImpl(self, node):
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
