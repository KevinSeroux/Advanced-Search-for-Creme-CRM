# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.forms import ModelMultipleChoiceField
from creme.creme_core.models import CremePropertyType, CremeProperty
from creme.creme_core.forms.widgets import UnorderedMultipleChoiceWidget

def add_property_field(form_instance):
    entity = form_instance._meta.model()
    entity_type_ID = entity.entity_type_id
    form_instance.fields['props'] = ModelMultipleChoiceField(label=_('Type of property'),
                                                             required=False,
                                                             queryset=CremePropertyType.objects.filter(subject_ctypes=entity_type_ID),
                                                             widget=UnorderedMultipleChoiceWidget)

def save_props(form_instance):
    prop_types = form_instance.cleaned_data['props']
    for prop_type in prop_types:
        CremeProperty.objects.create(type=prop_type,
                                     creme_entity=form_instance.instance)
