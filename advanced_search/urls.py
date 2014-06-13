# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('creme.advanced_search.views',
    (r'^$', 'search'),
)
