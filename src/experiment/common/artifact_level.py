from typing import Dict, List, Tuple


class ArtifactLevel:
    def __init__(self, sources: Dict[str, str], targets: Dict[str, str], links: List[Tuple[str, str]]):
        self.sources = sources
        self.targets = targets
        self.links = links
