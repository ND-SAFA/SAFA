from transformers import DataCollatorWithPadding, AutoTokenizer, default_data_collator

from jobs.job_args import JobArgs


# TODO
class TraceData:

    def __init__(self, s_arts, t_arts, links):
        self.s_arts = s_arts
        self.t_arts = t_arts
        self.links = links

    def _get_data_collator(self, tokenizer: AutoTokenizer, args: JobArgs):
        data_collator = (
            default_data_collator
            if args.pad_to_max_length
            else DataCollatorWithPadding(
                tokenizer, pad_to_multiple_of=8 if args.fp16 else None
            )
        )
        return data_collator

    def make_dataset(self, tokenizer: AutoTokenizer, args: JobArgs):
        data_collator = self._get_data_collator(tokenizer, args)
