class SDK(object):

    # required
    @classmethod
    def dumpHierarchy(cls):
        """ dump hierarchy of UI and 3d Models"""
        raise NotImplementedError

    @staticmethod
    def _get_screen_size():
        """get screen_size to count pos and size of Node in percentage"""
        raise NotImplementedError

    @staticmethod
    def _get_root(self):
        """get root node of UI or Models to dump"""
        raise NotImplementedError

    # optional
    @classmethod
    def snapshot():
        """get screenshot"""
        raise NotImplementedError

    # optional
    @classmethod
    def click(cls, xp, yp):
        """click on screen, xp & xp is in percentage of screen"""
        raise NotImplementedError

    # optional
    @classmethod
    def swipe(cls):
        """swipe on screen, xp & xp is in percentage of screen"""
        raise NotImplementedError

    # optional
    @classmethod
    def select(cls, query):
        """select in sdk to speed up, to replace dumpHierarchy"""
        raise NotImplementedError


class Node(object):

    required = []
    optional = []

    def getParent(self):
        """get parent node"""
        raise NotImplementedError

    def getChildren(self):
        """get chilren nodes"""
        raise NotImplementedError

    def getAttr(self, name):
        """get attr of node"""
        raise NotImplementedError

    def enumAttrs(self):
        """get all attrs of node"""
        raise NotImplementedError
