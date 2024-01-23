import random
import os

def random_query(workload, params, **kwargs):
    # choose a suitable index: if there is only one defined for this workload                                                                                                                                                                                                             
    # choose that one, but let the user always override index and type.                                                                                                                                                                                                                   
    if len(workload.indices) == 1:
        default_index = workload.indices[0].name
        if len(workload.indices[0].types) == 1:
            default_type = workload.indices[0].types[0].name
        else:
            default_type = None
    else:
        default_index = "_all"
        default_type = None

    index_name = params.get("index", default_index)
    type_name = params.get("type", default_type)
    model_id = params.get("model_id", None)
    script_dir=os.path.dirname(os.path.realpath(__file__))
    random_query = random.choice(open(script_dir + '/queries.txt').readlines())

    return {
        "body": {
            "track_total_hits": True,
            "_source": {
                "excludes": [
                    "passage_embedding"
                ]
            },
            "query": {
                "neural": {
                    "passage_embedding": {
                        "query_text": random_query,
                        "model_id": model_id,
                        "k": 5
                    }
                }
            }
        },
        "index": index_name,
        "type": type_name,
        "cache": params.get("cache", False)
    }


def register(registry):
    registry.register_param_source("semantic-search-random-source", random_query)

