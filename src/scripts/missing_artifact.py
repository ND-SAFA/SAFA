import argparse
import os
import sys
from typing import List

import torch
from datasets import Dataset
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, DataCollatorForSeq2Seq, EncoderDecoderModel, Seq2SeqTrainer, \
    Seq2SeqTrainingArguments

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

from data.creators.safa_dataset_creator import SafaDatasetCreator
from data.datasets.trace_dataset import TraceDataset

BOS_TOKEN_ID = 101
EOS_TOKEN_ID = 102
MAX_SEQUENCE_LENGTH = 50
MAX_INPUT_LENGTH = 126


class AutoEncoder:
    """
    BERT Encoder-Decoder for sequence-to-sequence tasks.
    """

    def __init__(self, base_model="bert-base-uncased", tensor_type="pt"):
        """
        Creates autoencoder using given base bert model and tensor types.
        :param base_model: The base bert model to use for encoder and decoders.
        :param tensor_type: "pt" or "tf"
        """
        self.base_model = base_model
        self.tensor_type = tensor_type
        self.model = EncoderDecoderModel.from_encoder_decoder_pretrained(base_model, base_model)
        self.tokenizer = BertTokenizer.from_pretrained(base_model)
        self.tokenizer_kwargs = {"add_special_tokens": False,
                                 "return_tensors": self.tensor_type,
                                 "padding": True,
                                 "truncation": True}
        self.model.config.decoder_start_token_id = self.tokenizer.cls_token_id
        self.model.config.pad_token_id = self.tokenizer.pad_token_id
        self.model.config.eos_token_id = self.tokenizer.sep_token_id
        self.model.config.vocab_size = self.model.config.encoder.vocab_size
        self.use_default_search()

    def use_default_search(self):
        self.model.config.max_length = 142
        self.model.config.min_length = 56
        self.model.config.no_repeat_ngram_size = 3
        self.model.config.early_stopping = True
        self.model.config.length_penalty = 2.0
        self.model.config.num_beams = 4

    def create_training_args(self, batch_size, output_path: str, **kwargs) -> Seq2SeqTrainingArguments:
        return Seq2SeqTrainingArguments(
            predict_with_generate=True,
            evaluation_strategy="epoch",
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            fp16=torch.cuda.is_available(),
            output_dir=output_path,
            logging_steps=100,
            eval_steps=100,
            save_total_limit=1,
            **kwargs
        )

    def tokenize(self, corpus: List[str]):
        """
        Tokenizes corpus with set tokenizer kwargs.
        :param corpus: List of sentences to tokenize.
        :return: TokenIds.
        """
        return self.tokenizer.batch_encode_plus(corpus, **self.tokenizer_kwargs)

    def compute_metrics(self, predictions):
        labels_ids = predictions.label_ids
        predicted_ids = predictions.predictions

        predicted_sentence = self.tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)
        label_sentence = self.tokenizer.batch_decode(labels_ids, skip_special_tokens=True)

        for source, generated in zip(label_sentence, predicted_sentence):
            print("Source:", source)
            print("Generated:", generated)
            print()

        return {
            "result": 42  # dummy metric for now
        }

    def create_dataset(self, sentences: List[str]):
        def pre_process(examples):
            model_inputs = self.tokenizer(examples["source"], max_length=MAX_INPUT_LENGTH, truncation=True)
            labels = self.tokenizer(examples["target"], max_length=MAX_INPUT_LENGTH, truncation=True)
            model_inputs["labels"] = labels["input_ids"]
            return model_inputs

        def create(s: List[str]):
            dataset = Dataset.from_dict({
                "source": s,
                "target": s
            })
            return dataset.map(pre_process, batched=True)

        return create(sentences)

    def train(self, output_path: str, source_sentences: List[str], target_sentences: List[str] = None, n_epochs=1,
              batch_size=4, val_size=.2) -> None:
        """
        Trains model to predict target sentences from sources.
        :param source_sentences: List of source sentences.
        :param target_sentences: List of target sentences.
        :param n_epochs: Number epochs to train for.
        :param batch_size: Size of the batches.
        """
        train_sentences, validation_sentences = train_test_split(source_sentences, test_size=val_size)
        train_data = self.create_dataset(train_sentences)
        val_data = self.create_dataset(validation_sentences)
        training_args = self.create_training_args(batch_size, output_path, num_train_epochs=n_epochs)
        data_collator = DataCollatorForSeq2Seq(self.tokenizer, self.model)
        trainer = Seq2SeqTrainer(
            model=self.model,
            args=training_args,
            train_dataset=train_data,
            eval_dataset=val_data,
            compute_metrics=self.compute_metrics,
            data_collator=data_collator
        )
        trainer.train()
        trainer.save_model()

    def test_autoencoder(self, test_sentences):

        test_token_ids = self.tokenize(test_sentences)
        generated_tokens = self.model.generate(test_token_ids)
        generated_sentences = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        print("-" * 15, "Eval", "-" * 15)
        print("Source")
        print("\n".join(test_sentences))
        print("Generated")
        print("\n".join(generated_sentences))

    def encode(self, sentences):
        token_ids = self.tokenize(sentences)
        return self.model.encoder.base_model(token_ids)[0]

    def decode(self, vector):
        """
        Decodes a vector into a sentence.
        :param vector: The vector to decode into sentence.
        :return: String representing decoded vector
        """
        predict_output = self.model.bert(vector).data
        n_sentences, seq_len, vocab_size = predict_output.shape
        output_sentences = []
        for sentence_index in range(n_sentences):
            sentence_tokens = []
            for word_index in range(seq_len):
                word_distribution = predict_output[sentence_index, word_index]
                token_id = torch.argmax(word_distribution).item()
                sentence_tokens.append(token_id)
            output_sentences.append(sentence_tokens)
        return self.tokenizer.batch_decode(output_sentences, skip_special_tokens=True)

    def corpus_vector(self, sentences: List[str]):
        """
        Calculates a representative vector for given corpus by concatenating embeddings of sentences in corpus.
        :param sentences: List of sentences.
        # TODO : Add different concatenations
        :return: Single vector representing corpus.
        """
        embeddings = self.encode(sentences)
        n_sentences, n_words, n_dim = embeddings.shape
        aggregate_embedding = torch.zeros((n_words, n_dim))
        for sentence_index in range(n_sentences):
            aggregate_embedding = aggregate_embedding + embeddings[sentence_index]
        embeddings = torch.reshape(aggregate_embedding, (1, n_words, n_dim))
        return embeddings

    def predict(self, sentence: str):
        # create ids of encoded input vectors
        input_ids = self.tokenizer(sentence, return_tensors="pt").input_ids
        decoder_input_ids = self.tokenizer(self.tokenizer.cls_token,
                                           add_special_tokens=False,
                                           return_tensors="pt").input_ids
        decoder_start_token = decoder_input_ids[0, 0].item()

        assert decoder_start_token == self.model.config.decoder_start_token_id, "`decoder_input_ids` should correspond to `model.config.decoder_start_token_id`"

        # pass input_ids to encoder and to decoder and pass BOS token to decoder to retrieve first logit
        outputs = self.model(input_ids, decoder_input_ids=decoder_input_ids, return_dict=True)
        encoded_sequence = (outputs.encoder_last_hidden_state,)
        lm_logits = outputs.logits

        running = True
        i = 0
        while running and not i > MAX_SEQUENCE_LENGTH:
            next_decoder_input_ids = torch.argmax(lm_logits[:, -1:], axis=-1)
            next_index = next_decoder_input_ids.item()
            if next_index == 0:
                break
            decoder_input_ids = torch.cat([decoder_input_ids, next_decoder_input_ids], axis=-1)
            lm_logits = self.model(None,
                                   encoder_outputs=encoded_sequence,
                                   decoder_input_ids=decoder_input_ids,
                                   return_dict=True).logits
            i += 1
        autoencoded_sentence = self.tokenizer.decode(decoder_input_ids[0], skip_special_tokens=True)
        print("Original", sentence)
        print("Generated:", autoencoded_sentence)


def read_project_artifacts(project_path: str) -> List[str]:
    safa_dataset_creator = SafaDatasetCreator(project_path)
    trace_dataset: TraceDataset = safa_dataset_creator.create()
    id2artifact = {}

    def add_artifact(artifact):
        artifact_id = artifact.id
        artifact_body = artifact.token
        if artifact_id not in id2artifact:
            id2artifact[artifact_id] = artifact_body

    for link_id, link in trace_dataset.links.items():
        target = link.target
        source = link.source

        add_artifact(target)
        add_artifact(source)
    return list(id2artifact.values())


if __name__ == "__main__":
    # A. Read arguments
    parser = argparse.ArgumentParser(
        prog='AutoEncoder for Project',
        description='AutoEncodes project.')
    parser.add_argument('project')
    parser.add_argument('export')
    parser.add_argument('-e', default=1, type=int)
    args = parser.parse_args()
    project_path = os.path.expanduser(args.project)

    # 1. Read Project
    project_artifacts = read_project_artifacts(project_path)
    source_project_artifacts: List[str] = project_artifacts
    print("Source:", len(source_project_artifacts))

    # 2. Train Model
    autoencoder = AutoEncoder()
    autoencoder.train(args.export, source_project_artifacts, n_epochs=args.e)
