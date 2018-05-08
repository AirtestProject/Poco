# coding=utf-8

from poco.utils.track import MotionTrack

__all__ = ['PendingGestureAction']


class PendingGestureAction(object):
    def __init__(self, pocoobj, uiproxy_or_pos):
        super(PendingGestureAction, self).__init__()
        self.pocoobj = pocoobj
        self.track = MotionTrack()
        if isinstance(uiproxy_or_pos, (list, tuple)):
            self.track.start(uiproxy_or_pos)
        else:
            self.track.start(uiproxy_or_pos.get_position())

    def hold(self, t):
        self.track.hold(t)
        return self

    def to(self, pos):
        if isinstance(pos, (list, tuple)):
            self.track.move(pos)
        else:
            uiobj = pos
            self.track.move(uiobj.get_position())
        return self

    def up(self):
        self.pocoobj.apply_motion_tracks([self.track])
