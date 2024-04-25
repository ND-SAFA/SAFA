from typing import Dict, List

import numpy as np

from tgen.tracing.ranking.sorters.vsm_sorter import VSMSorter


def vsm_tracer(state: Dict, source_artifact: List[str], target_artifact: List[str]):
    artifact_map = {a: a for a in source_artifact + target_artifact}

    source2predictions = VSMSorter.sort(source_artifact, target_artifact, artifact_map, return_scores=True)
    matrix = []
    for source, predictions in source2predictions.items():
        matrix.append(predictions[1])
    similarity_matrix = np.array(matrix)
    return similarity_matrix
