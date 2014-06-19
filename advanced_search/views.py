# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from creme.creme_core.models import CremeProperty, CremePropertyType
from search import advanced_search

@login_required
def search(request):
    t_ctx = {} # This the dict which will be sended to the template

    # If the user proceed to a research
    if request.method == 'POST':
        post_datas          = request.POST

        post_research_terms = post_datas.get('research_terms')
        post_models_IDs     = post_datas.getlist('models_IDs')
        post_props_IDs      = post_datas.getlist('props')

        is_datas_valid = True
    
        if not post_props_IDs:

            if not post_research_terms:
                t_ctx['error_message'] = _(u"If no properties are selected, the "
                                             "terms field is required")
                is_datas_valid = False

            elif len(post_research_terms) <3:
                t_ctx['error_message'] = _(u"Please enter at least 3 characters")
                is_datas_valid = False

        if is_datas_valid == True:
            total, results, models_list = advanced_search \
            (post_models_IDs, post_research_terms, post_props_IDs, request.user)

            for result in results:
                for entity in result['entities']:
                    props_IDs = CremeProperty.objects.filter(creme_entity_id =
                                                             entity.id)
                    props = CremeProperty.objects.filter(id = props_IDs)
                    entity.props = props

            t_ctx['total'] = total
            t_ctx['results'] = results
            t_ctx['research'] = post_research_terms
            t_ctx['models'] = models_list
            t_ctx['props'] = []

            for post_prop_ID in post_props_IDs:
               prop = CremePropertyType.objects.get(id=post_prop_ID)
               t_ctx['props'].append(prop.text)

        return HttpResponse(render_to_string \
          ("advanced_search/search_results.html", t_ctx, \
          context_instance=RequestContext(request)))

    else: # If the user request the advanced search page):
        # TODO: Check if the properties are sent such as the models list

        # To send the list of properties available to the template
        t_ctx = {'props': CremePropertyType.objects.all()}
        return HttpResponse(render_to_string \
          ("advanced_search/advanced_search.html", t_ctx,
          context_instance=RequestContext(request)))
