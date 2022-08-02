import torch
from torch import nn
from torch.nn import CrossEntropyLoss
from transformers import AutoModel, BertPreTrainedModel


class AvgPooler(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.pooler = nn.AdaptiveAvgPool2d((1, config.hidden_size))

    def forward(self, hidden_states):
        return self.pooler(hidden_states).view(-1, self.hidden_size)


class RelationClassifyHeader(nn.Module):
    """
    use averaging pooling across tokens to replace first_token_pooling.
    """

    def __init__(self, config):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.s_pooler = AvgPooler(config)
        self.t_pooler = AvgPooler(config)

        self.dense = nn.Linear(config.hidden_size * 3, config.hidden_size)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.output_layer = nn.Linear(config.hidden_size, 2)

    def forward(self, s_hidden, t_hidden):
        pool_s_hidden = self.s_pooler(s_hidden)
        pool_t_hidden = self.t_pooler(t_hidden)
        diff_hidden = torch.abs(pool_s_hidden - pool_t_hidden)
        concated_hidden = torch.cat((pool_s_hidden, pool_t_hidden), 1)
        concated_hidden = torch.cat((concated_hidden, diff_hidden), 1)

        x = self.dropout(concated_hidden)
        x = self.dense(x)
        x = torch.tanh(x)
        x = self.dropout(x)
        x = self.output_layer(x)
        return x


class BertTraceSiamese(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.lm = AutoModel.from_config(config)
        self.classifier = RelationClassifyHeader(config)
        self.init_weights()

    def forward(
            self,
            s_input_ids=None,
            s_attention_mask=None,
            t_input_ids=None,
            t_attention_mask=None,
            labels=None,
            **kwargs
    ):
        s_hidden = self.lm(
            s_input_ids, attention_mask=s_attention_mask
        ).last_hidden_state
        t_hidden = self.lm(
            t_input_ids, attention_mask=t_attention_mask
        ).last_hidden_state

        logits = self.cls(s_hidden=s_hidden, t_hidden=t_hidden)
        output_dict = {}
        if labels is not None:
            loss_fct = CrossEntropyLoss()
            rel_loss = loss_fct(logits.view(-1, 2), labels.view(-1))
            output_dict["loss"] = rel_loss
        output_dict["logits"] = torch.softmax(logits, 1)
        return output_dict  # (rel_loss), rel_score

    def get_sim_score(self, s_hidden, t_hidden):
        logits = self.classifier(t_hidden=s_hidden, s_hidden=t_hidden)
        sim_scores = torch.softmax(logits, 1).data.tolist()
        return [x[1] for x in sim_scores]



