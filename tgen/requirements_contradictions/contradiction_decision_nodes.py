from tgen.common.util.supported_enum import SupportedEnum
from tgen.decision_tree.abstract_node import AbstractNode


class SupportedContradictionDecisionNodes(SupportedEnum):
    NONE = AbstractNode("No Contradiction")
    SIMPLEX_CONTRADICTION = AbstractNode("Simplex Contradiction")
    IDEM_CONTRADICTION = AbstractNode("Idem Contradiction")
    ALIUS_CONTRADICTION = AbstractNode("Alius Contradiction")
