# -*- coding: utf-8 -*-

from functools import partial

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from creme.creme_core.core.search import Searcher
from creme.creme_core.utils import get_ct_or_404
from creme.creme_core.models import EntityCredentials, CremeProperty, \
                                    CremePropertyType


@login_required
def search(request):
    t_ctx = {} # This the dict which will be sended to the template

    # If the user proceed to a research
    if request.method == 'POST':
        post_datas          = request.POST

        post_research_terms = post_datas.get('research_terms')
        post_models_IDs     = post_datas.getlist('models_IDs')
        post_props_IDs      = post_datas.getlist('props')

        models  = []
        results = []
        total   = 0

        is_datas_valid = True
    
        if not post_props_IDs:

            if not post_research_terms:
                t_ctx['error_message'] = _(u"If no properties are selected, the "
                                             "terms field is required")
                is_datas_valid = False

            elif len(post_research_terms) < 3:
                t_ctx['error_message'] = _(u"Please enter at least 3 characters")
                is_datas_valid = False

        if is_datas_valid == True:

            # We will need to access to model class so we retrieve it with the id
            if not post_models_IDs:
                # Add all the existing models
                models.extend(creme_registry.iter_entity_models())
            else:
                # Add just the requested models
                for post_model_ID in post_models_IDs:
                    models.append(get_ct_or_404(post_model_ID).model_class())

            if(len(models) > 1): # Useless to sort when we have only one model
                models.sort(key=lambda m: m._meta.verbose_name)
    
            user = request.user
            filter_viewable = partial(EntityCredentials.filter, user=user)
            searcher = Searcher(models, user)
    
            for model in models:
                # To retrieve the entities the user is authorized to see
                entities = list(filter_viewable \
                  (queryset=searcher.search(model, post_research_terms)))

                # Here we will remove the entities which don't have the
                # requested properties
                if post_props_IDs:
                    
                    # We need to add [:] because some entity will be removed
                    # Otherwise some entities will not be processed
                    # http://stackoverflow.com/a/1352908
                    for entity in entities[:]:
                        # props is the list of the properties related to the
                        # entity and not the properties the user is looking for
                        props = list(CremeProperty.objects.filter \
                          (creme_entity = entity.id))

                        # If the entity have some properties
                        if len(props) > 0:
                            count_properties_found = len(props)

                            # We decrement a number if a requested property is
                            # not found. TODO: Better explain the algorithm...
                            for prop in props:
                                if post_props_IDs.count(prop.type_id) == 0:
                                    count_properties_found -= 1

                            if count_properties_found < len(post_props_IDs):
                                entities.remove(entity)

                        else: # We remove it because we are looking for props
                            entities.remove(entity)

                total += len(entities)
                results.append({'model':    model,
                                'fields':   searcher.get_fields(model),
                                'entities': entities,
                               }
                              )

            t_ctx['total'] = total
            t_ctx['results'] = results
            t_ctx['research'] = post_research_terms
            t_ctx['models'] = [model._meta.verbose_name for model in models]


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
