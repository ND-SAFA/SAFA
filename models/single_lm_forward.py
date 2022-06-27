import torch
from torch.nn import CrossEntropyLoss


def single_lm_forward(
        model,
        cls_header,
        num_labels,
        input_ids,
        attention_mask,
        token_type_ids,
        labels=None,
        **kwargs
):
    hidden = model(
        input_ids=input_ids,
        attention_mask=attention_mask,
        token_type_ids=token_type_ids,
    ).last_hidden_state
    logits = cls_header(hidden)
    output_dict = dict()

    if labels is not None:
        loss_fct = CrossEntropyLoss()  # loss fct need logits without softmax
        loss = loss_fct(logits.view(-1, num_labels), labels.view(-1))
        output_dict["loss"] = loss
    output_dict["logits"] = torch.softmax(logits, 1)
    return output_dict
