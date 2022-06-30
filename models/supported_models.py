import enum
from bert_trace_single import BertTraceSingleModelGenerator
from models.bert_trace_siamese import BertTraceSiameseModelGenerator
from models.electra_trace_single import ElectraTraceSingleModelGenerator


class SupportedModels(enum):
    BERT_TRACE_SIAMESE = 'bert_trace_siamese'
    BERT_TRACE_SINGLE = 'bert_trace_single'
    ELECTRA_TRACE_SINGLE = 'electra_trace_single'


MODEL_GENERATORS = {SupportedModels.BERT_TRACE_SINGLE: BertTraceSingleModelGenerator,
                    SupportedModels.BERT_TRACE_SIAMESE: BertTraceSiameseModelGenerator,
                    SupportedModels.ELECTRA_TRACE_SINGLE: ElectraTraceSingleModelGenerator}
