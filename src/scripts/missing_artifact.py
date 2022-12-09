import argparse
import math
import os
import sys
from typing import List

import torch
from dotenv import load_dotenv
from tqdm import tqdm
from transformers import BertTokenizer, EncoderDecoderModel

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

from data.creators.safa_dataset_creator import SafaDatasetCreator
from data.datasets.trace_dataset import TraceDataset

BOS_TOKEN_ID = 101
EOS_TOKEN_ID = 102


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

    def tokenize(self, corpus: List[str]):
        """
        Tokenizes corpus with set tokenizer kwargs.
        :param corpus: List of sentences to tokenize.
        :return: TokenIds.
        """
        return self.tokenizer.batch_encode_plus(corpus, **self.tokenizer_kwargs).input_ids

    def train(self, source_sentences: List[str], target_sentences: List[str] = None, n_epochs=1, batch_size=4) -> None:
        """
        Trains model to predict target sentences from sources.
        :param source_sentences: List of source sentences.
        :param target_sentences: List of target sentences.
        :param n_epochs: Number epochs to train for.
        :param batch_size: Size of the batches.
        """
        if target_sentences is None:
            target_sentences = source_sentences
        assert len(source_sentences) == len(target_sentences), "Expected source length to match target length."

        n_sentences = len(source_sentences)
        n_batches = math.ceil(n_sentences / batch_size)
        for epoch in range(n_epochs):
            for batch_index in tqdm(range(n_batches)):
                start_index = batch_size * batch_index
                end_index = start_index + batch_size
                if end_index > n_sentences - 1:
                    end_index = n_sentences - 1
                batch_sentences = source_sentences[start_index: end_index]
                batch_labels = target_sentences[start_index: end_index]
                input_ids = self.tokenize(batch_sentences)
                labels = self.tokenize(batch_labels)
                loss = self.model(input_ids=input_ids, decoder_input_ids=labels, labels=labels).loss
                loss.backward()
            self.predict(source_sentences[0])

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
        while running and not i > 100:
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
    parser.add_argument('-e', default=1, type=int)
    args = parser.parse_args()
    project_path = os.path.expanduser(args.project)

    # 1. Read Project
    project_artifacts = read_project_artifacts(project_path)[:]
    source_project_artifacts: List[str] = project_artifacts
    print("Source:", len(source_project_artifacts))

    # 2. Train Model
    autoencoder = AutoEncoder()
    autoencoder.train(source_project_artifacts, n_epochs=args.e)
