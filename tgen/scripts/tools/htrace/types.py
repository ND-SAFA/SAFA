from typing import *

import numpy as np

SimilarityMatrixType = np.ndarray
TracerMethodType = Callable[[Dict, List[str], List[str]], SimilarityMatrixType]
