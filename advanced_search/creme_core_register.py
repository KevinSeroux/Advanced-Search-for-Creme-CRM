# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from creme.creme_core.registry import creme_registry
from creme.creme_core.gui import creme_menu, quickforms_registry
from creme.creme_core.models.creme_property import CremePropertyType
from creme.creme_core.forms import CremeEntityForm
from creme.advanced_search.forms.creme_property import CremePropertyTypeQuickAddForm
from creme.advanced_search.forms.base import add_property_field, save_props

creme_registry.register_app('advanced_search', _(u'Advanced searching'))
creme_menu.register_app('advanced_search', '/advanced_search/', _(u'Advanced search'), force_order=2)

quickforms_registry.register(CremePropertyType, CremePropertyTypeQuickAddForm)

CremeEntityForm.add_post_init_callback(add_property_field)
CremeEntityForm.add_post_save_callback(save_props)
