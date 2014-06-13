# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from creme.creme_core.registry import creme_registry
from creme.creme_core.gui.menu import creme_menu


creme_registry.register_app('advanced_search', _(u'Advanced searching'))
creme_menu.register_app('advanced_search', '/advanced_search/', _(u'Advanced search'), force_order=2)
