# coding=utf-8

from . import AirtestPoco
from airtest.core.main import set_serialno


if __name__ == '__main__':
    set_serialno()
    p = AirtestPoco("g18")
    p(text="化生寺").click()
