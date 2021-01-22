# coding=utf-8

from airtest.core.api import connect_device


def UnityEditorWindow():
    dev = connect_device("Windows:///?class_name=UnityContainerWndClass&title_re=.*Unity.*")
    game_window = dev.app.top_window().child_window(title="UnityEditor.GameView")
    dev._top_window = game_window.wrapper_object()
    dev.focus_rect = (0, 40, 0, 0)
    return dev
