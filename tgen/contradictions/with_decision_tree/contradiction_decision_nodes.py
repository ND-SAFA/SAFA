from tgen.common.util.supported_enum import SupportedEnum
from tgen.decision_tree.nodes.leaf_node import LeafNode


class SupportedContradictionDecisionNodes(SupportedEnum):
    NONE = LeafNode("No Contradiction")
    SIMPLEX_CONTRADICTION = LeafNode("Simplex Contradiction")
    IDEM_CONTRADICTION = LeafNode("Idem Contradiction")
    ALIUS_CONTRADICTION = LeafNode("Alius Contradiction")
