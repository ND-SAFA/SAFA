from typing import Optional

import torch
from torch.nn import CrossEntropyLoss
from transformers import PreTrainedModel
from transformers.models.electra.modeling_electra import ElectraClassificationHead

from config.constants import LOGITS, LOSS

"""
Attention Mask
----------------------------------------------
Mask to avoid performing attention on padding token indices. Mask values selected in [0, 1]:
    - 1 for tokens that are not masked,
    - 0 for tokens that are masked.
    

Token Type Ids
----------------------------------------------
Segment token indices to indicate first and second portions of the inputs. Indices are selected in [0, 1]:
0 corresponds to a sentence A token,
1 corresponds to a sentence B token.


Labels
----------------------------------------------
Labels for computing the masked language modeling loss. 
Indices should be in [-100, 0, ..., config.vocab_size] (see input_ids docstring) 
Tokens with indices set to -100 are ignored (masked), the loss is only computed for the tokens with labels 
in [0, ..., config.vocab_size] next_sentence_label (torch.LongTensor of shape (batch_size,), optional): 
Labels for computing the next sequence prediction (classification) loss. Input should be a sequence pair 
(see input_ids docstring) Indices should be in [0, 1]:

    - 0 indicates sequence B is a continuation of sequence A,
    - 1 indicates sequence B is a random sequence. kwargs (Dict[str, any], optional, defaults to {}): Used to hide legacy arguments that have been deprecated.
    
Input Ids
----------------------------------------------
Indices of input sequence tokens in the vocabulary. See PreTrainedTokenizer.encode() and PreTrainedTokenizer.call()
for details.

"""


def single_model_forward_pass(
        model: PreTrainedModel,
        cls_header: ElectraClassificationHead,
        num_labels: int,
        input_ids: Optional[torch.Tensor],
        attention_mask: Optional[torch.Tensor],
        token_type_ids: Optional[torch.LongTensor],
        labels=None,
        **kwargs
):
    """
    Performs a forward pass on given model.
    Documentation gathered from: https://huggingface.co/docs/transformers/model_doc/bert.
    :param model: The model to perform the pass on.
    :param cls_header: Classification header.
    :param num_labels: # of labels used in classification performed.
    :param input_ids:  Indices of input sequence tokens in the vocabulary. Indices can be obtained using BertTokenizer.
    :param attention_mask: (torch.FloatTensor of shape (batch_size, sequence_length), optional)
    :param token_type_ids:  (torch.LongTensor of shape (batch_size, sequence_length), optional)
    :param labels: (torch.LongTensor of shape (batch_size, sequence_length), optional)
    :return:
    """
    hidden = model(
        input_ids=input_ids,
        attention_mask=attention_mask,
        token_type_ids=token_type_ids,
    ).last_hidden_state
    logits = cls_header(hidden)
    return calculate_softmax_from_logits(logits, num_labels, labels)


def calculate_softmax_from_logits(logits: torch.FloatTensor,
                                  num_labels,
                                  labels: Optional[torch.LongTensor] = None,
                                  ):
    """
    Calculates softmax of given logits. If labels is defined then  loss is calculated
    using cross entropy function.
    :param logits: The similarity scores predicted for input.
    :param num_labels: The number of labels used in the classification.
    :param labels: The predicted labels for the logits given.
    :return:
    """
    output_dict = dict()
    if labels is not None:
        loss_fct = CrossEntropyLoss()  # loss fct need logits without softmax
        loss = loss_fct(logits.view(-1, num_labels), labels.view(-1))
        output_dict[LOSS] = loss
    output_dict[LOGITS] = torch.softmax(logits, 1)
    return output_dict
