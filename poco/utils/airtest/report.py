# -*- coding: utf-8 -*-
import os
import airtest.report.report as report
LOGDIR = "log"
poco_func = ["record_ui"]

old_trans_desc = report.LogToHtml._translate_desc
old_analyse = report.LogToHtml._analyse
old_translate_title = report.LogToHtml._translate_title


def new_analyse(self):

    for log in self.log:
        if log["data"]["name"] == "record_ui":
            log["depth"] = 2

    trans_steps = old_analyse(self)
    return trans_steps


def new_translate_desc(self, step, code):
    trans = old_trans_desc(self, step, code)

    poco_ui = ""
    if "__children__" in step:
        for item in step["__children__"]:
            if item["data"]["name"] == "record_ui":
                poco_ui = item["data"]["call_args"]["ui"]

    if poco_ui:
        name = step['data']['name']
        desc = {
            "touch": "Touch %s" % poco_ui,
            "swipe": "Swipe from %s" % poco_ui,
            "set_text": "Set %s of text" % poco_ui
        }

        ret = desc.get(name)
        if callable(ret):
            ret = ret()
        return ret

    else:
        return trans


def new_translate_title(self, name, step):
    title = old_translate_title(self, name, step)

    poco_title = False
    if "__children__" in step:
        for item in step["__children__"]:
            if item["data"]["name"] == "record_ui":
                poco_title = True

    if poco_title:
        title = {
            "touch": u"Poco Click",
            "swipe": u"Poco Swipe",
            "set_text": u"Poco Set Text"
        }
        return title.get(name, name)
    else:
        return title


report.LogToHtml._translate_desc = new_translate_desc
report.LogToHtml._analyse = new_analyse
report.LogToHtml._translate_title = new_translate_title
