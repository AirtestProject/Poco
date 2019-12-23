# coding=utf-8

from airtest.core.api import connect_device


def UE4EditorWindow():
    dev = connect_device("Windows:///?class_name=UnrealWindow&title_re=.*Game Preview Standalone.*")
    game_window = dev.app.top_window()
    dev._top_window = game_window.wrapper_object()
    dev.focus_rect = (5, 29, 5, 5)
    return dev
