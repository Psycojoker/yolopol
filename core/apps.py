# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.core.checks import register

from checks.browser_libs import libs_check
from checks.less_errors import less_check


class CoreAppConfig(AppConfig):
    name = 'core'

    def ready(self):
        super(CoreAppConfig, self).ready()
        register()(less_check)
        register()(libs_check)
