# -*- coding: utf-8 -*-

from django.forms import CharField, BooleanField
from django.utils.translation import ugettext_lazy as _, ugettext

from creme.creme_core.forms import MultiEntityCTypeChoiceField
from creme.creme_core.forms.base import CremeModelForm, CremeEntityForm
from creme.creme_core.models.creme_property import CremePropertyType

class CremePropertyTypeQuickAddForm(CremeModelForm):
    text           = CharField(label=_(u'Text'), help_text=_("For example: 'is pretty'"))
    subject_ctypes = MultiEntityCTypeChoiceField(label=_(u'Related to types of entities'),
                                                 help_text=_(u'No selected type means that all types are accepted'),
                                                 required=False,
                                                 )

    class Meta(CremeEntityForm.Meta):
        model = CremePropertyType
        # What's is_copiable?
        exclude = ('is_custom', 'id', 'is_copiable')

    def clean_text(self):
        text = self.cleaned_data['text']

        if CremePropertyType.objects.filter(text=text).exists(): #TODO: unique constraint in model too ??
            raise ValidationError(ugettext(u"A property type with this name already exists"))

        return text

    def save(self):
        get_data = self.cleaned_data.get
        CremePropertyType.create('creme_config-userproperty',
                                 get_data('text'), get_data('subject_ctypes'),
                                 is_custom=True, generate_pk=True,
                                 )
