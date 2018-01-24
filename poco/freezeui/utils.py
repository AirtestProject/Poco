# coding=utf-8

from poco.freezeui.hierarchy import FreezedUIDumper, FreezedUIHierarchy


__all__ = ['create_immutable_hierarchy', 'create_immutable_dumper']


def create_immutable_hierarchy(hierarchy_dict):
    dumper = create_immutable_dumper(hierarchy_dict)
    return FreezedUIHierarchy(dumper)


def create_immutable_dumper(hierarchy_dict):
    class ImmutableFreezedUIDumper(FreezedUIDumper):
        def dumpHierarchy(self):
            return hierarchy_dict

    return ImmutableFreezedUIDumper()
