# coding=utf-8

from poco.sdk.Attributor import Attributor
from poco.sdk.exceptions import UnableToSetAttributeException


class StdAttributor(Attributor):
    def __init__(self, client):
        super(StdAttributor, self).__init__()
        self.client = client

    def setAttr(self, node, attrName, attrVal):
        if attrName == 'text':
            if type(node) in (list, tuple):
                node = node[0]
            instance_id = node.getAttr('_instanceId')
            if instance_id:
                success = self.client.call('SetText', instance_id, attrVal)
                if success:
                    return True
        raise UnableToSetAttributeException(attrName, node)
