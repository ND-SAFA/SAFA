from typing import Dict, List

from tgen.common.util.list_util import ListUtil
from tgen.tracing.ranking.sorters.i_sorter import iSorter
from tgen.tracing.ranking.sorters.transformer_sorter import TransformerSorter
from tgen.tracing.ranking.sorters.vsm_sorter import VSMSorter


class CombinedSorter(iSorter):
    @staticmethod
    def sort(*args, **kwargs) -> Dict[str, List]:
        vsm_sorter = VSMSorter()
        vsm_output = vsm_sorter.sort(*args, **kwargs)

        embedding_sorter = TransformerSorter()
        embedding_output = embedding_sorter.sort(*args, **kwargs)

        query_ids = vsm_output.keys()

        sorter_map = {}
        for query_id in query_ids:
            vsm_query_map = {a_id: a_score for a_id, a_score in zip(*vsm_output[query_id])}
            embedding_query_map = {a_id: a_score for a_id, a_score in zip(*embedding_output[query_id])}

            query_children_ids = vsm_query_map.keys()

            query_output_ids = []
            query_output_scores = []
            for child_id in query_children_ids:
                vsm_score = vsm_query_map[child_id]
                embedding_score = embedding_query_map[child_id]

                query_output_ids.append(child_id)
                query_output_scores.append(max(vsm_score, embedding_score))

            query_output_ids, query_output_scores = ListUtil.sort_by(query_output_ids, query_output_scores, reverse=True)
            sorter_map[query_id] = (query_output_ids, query_output_scores)

        return sorter_map
