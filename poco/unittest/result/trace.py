# coding=utf-8

import sys
import time


def make_tracer(filename):
    def tracer(frame, event, arg):
        if event == 'line' and filename == frame.f_code.co_filename:
            line_num = frame.f_lineno
            # TODO 定一下标准格式
            print(time.time(), line_num)
            return None
        return tracer
    return tracer


def start_line_tracing(filename):
    sys.settrace(make_tracer(filename))
