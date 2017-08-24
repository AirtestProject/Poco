# coding=utf-8

import inspect

from poco.unittest.case import PocoTestCase
from poco.unittest.runner import PocoTestRunner
from poco.unittest.suite import PocoTestSuite
from poco.unittest.result.trace import start_line_tracing


__author__ = 'lxn3032'


def has_override(method, subCls, baseCls):
    return getattr(subCls, method).__func__ is not getattr(baseCls, method).__func__


def main():
    current_frame = inspect.currentframe()
    caller = current_frame.f_back
    test_case_filename = caller.f_code.co_filename
    caller_scope = caller.f_locals

    # 这部分代码放到loader里
    Cases = [v for k, v in caller_scope.items() if
             type(v) is type and
             v is not PocoTestCase and
             issubclass(v, PocoTestCase) and
             has_override("runTest", v, PocoTestCase)
             ]
    suite = PocoTestSuite()
    for Case in Cases:
        suite.addTest(Case())
    runner = PocoTestRunner()
    start_line_tracing(test_case_filename)
    runner.run(suite)
