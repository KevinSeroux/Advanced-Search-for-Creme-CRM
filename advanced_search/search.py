# -*- coding: utf-8 -*-

from functools import partial

from creme.creme_core.utils import get_ct_or_404
from creme.creme_core.core.search import Searcher
from creme.creme_core.registry import creme_registry
from creme.creme_core.models import EntityCredentials, CremeProperty, \
                                    CremePropertyType

def advanced_search(models_IDs, research_terms, props_IDs, user):
    total = 0
    results = []
    models = []

    # We will need to access to model class so we retrieve it with the id
    if not models_IDs:
        # Add all the existing models
        models.extend(creme_registry.iter_entity_models())
    else:
        # Add just the requested models
        for model_ID in models_IDs:
            models.append(get_ct_or_404(model_ID).model_class())

    if(len(models) > 1): # Useless to sort when we have only one model
        models.sort(key=lambda m: m._meta.verbose_name)
    
    filter_viewable = partial(EntityCredentials.filter, user=user)
    searcher = Searcher(models, user)
    
    for model in models:
        # To retrieve the entities the user is authorized to see
        entities = list(filter_viewable \
                            (queryset=searcher.search(model, research_terms)))

        # Here we will remove the entities which don't have the
        # requested properties
        if props_IDs:
            
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
                        if props_IDs.count(prop.type_id) == 0:
                            count_properties_found -= 1

                    if count_properties_found < len(props_IDs):
                        entities.remove(entity)

                else: # We remove it because we are looking for props
                    entities.remove(entity)

        total += len(entities)
        results.append({'model':    model,
                        'fields':   searcher.get_fields(model),
                        'entities': entities,
                        }
                       )

    models_list = [model._meta.verbose_name for model in models]

    return total, results, models_list
