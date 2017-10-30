#!/usr/bin/env
# -*- coding: utf-8 -*-
"""parse apk file class, inherit from axmlparserpy."""
import os
from pydash import _


class APKParse(object):
    """APK parse."""

    def __init__(self, filename):
        """Init method."""
        super(APKParse, self).__init__()
        self.filename = filename
        self.valid_zip = False

        parse_data = self.get_aapt_parse_data('package')
        self.parse_dict = dict(item.split('=') for item in _.head(parse_data).split(' '))

    @property
    def package(self):
        package_name = self.parse_dict.get('name')
        if not package_name:
            raise RuntimeError('Cannot get package name from "{}"'.format(self.filename))
        return package_name

    @property
    def versionCode(self):
        vc = self.parse_dict.get('versionCode')
        if not vc:
            raise RuntimeError('Cannot get versionCode from "{}"'.format(self.filename))
        return int(vc)

    def get_raw(self):
        """Get raw data."""
        with open(self.filename, 'rb') as f:
            return f.read()

    def get_aapt_parse_data(self, app_type):
        """Get aapt parse data."""
        aapt_line = "aapt dump badging %s | grep '%s' | awk -F ':' \
            '{print $2}'" % (self.filename, app_type)
        aapt_data = os.popen(aapt_line).read().splitlines()
        parse_data = [d.replace("'", '').strip() for d in aapt_data if d]
        return parse_data

    def parse_package_version(self):
        """Parse package and version from apk."""
        parse_data = self.get_aapt_parse_data('package')
        package, version = '', ''
        if not parse_data:
            return package, version
        parse_dict = dict(
            item.split('=') for item in _.head(parse_data).split(' '))
        package = parse_dict.get('name', '')
        version = parse_dict.get('versionName', '')
        return package, version

    def parse_app_name(self):
        """Parse app name form apk."""
        parse_data = self.get_aapt_parse_data('application-label')
        app_name = _.head(parse_data) if parse_data else ''
        return app_name.decode("utf8")
