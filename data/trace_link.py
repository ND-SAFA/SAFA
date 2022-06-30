class Artifact:

    def __init__(self, id_: str, token: str):
        self.id_ = id_
        self.token = token


class TraceLink:

    def __init__(self, source: Artifact, target: Artifact, is_linked: bool = False):
        self.source = source
        self.target = target
        self.id_ = self.generate_link_id(self.source.id_, self.target.id_)
        self.is_linked = is_linked

    @staticmethod
    def generate_link_id(source_id: str, target_id: str) -> int:
        return hash(source_id) + hash(target_id)

    def __hash__(self):
        return hash(self.id_)


