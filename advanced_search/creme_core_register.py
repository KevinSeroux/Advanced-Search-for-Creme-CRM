# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from creme.creme_core.registry import creme_registry
from creme.creme_core.gui import creme_menu, quickforms_registry
from creme.creme_core.models.creme_property import CremePropertyType
from creme.advanced_search.forms.creme_property import CremePropertyTypeQuickAddForm


creme_registry.register_app('advanced_search', _(u'Advanced searching'))
creme_menu.register_app('advanced_search', '/advanced_search/', _(u'Advanced search'), force_order=2)

quickforms_registry.register(CremePropertyType, CremePropertyTypeQuickAddForm)
