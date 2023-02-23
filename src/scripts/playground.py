import os.path

import pandas as pd
from transformers import AutoTokenizer, RobertaTokenizer

if __name__ == "__main__":
    MAX_LENGTH = 4096
    tokenizer: RobertaTokenizer = AutoTokenizer.from_pretrained("roberta-base")
    dataset_path = os.path.expanduser("~/desktop/safa/datasets/iceoryx")

    issue_path = os.path.join(dataset_path, "issue.csv")
    issues_df = pd.read_csv(issue_path)
    print("Issues:", len(issues_df))

    code_path = os.path.join(dataset_path, "code.csv")
    code_df = pd.read_csv(code_path)
    print("Code:", len(code_path))

    issue = issues_df.sample(n=1).iloc[0]
    issue_id = issue["id"]
    issue_body = issue["content"]

    code = code_df.sample(n=1).iloc[0]
    code_id = code["id"]
    code_body = code["content"]
    print("-" * 25)
    print("Issue ID:", issue_id)
    print("Issue words:", len(issue_body.split(" ")))
    print("-" * 25)
    print("Code ID:", code_id)
    print("Code words:", len(code_body.split(" ")))

    encoded_trace = tokenizer(text=issue_body,
                              text_pair=code_body,
                              truncation=True,
                              max_length=MAX_LENGTH,
                              padding="max_length",
                              add_special_tokens=True)
    print()
    decoded_trace = tokenizer.decode(encoded_trace["input_ids"])
    sentences = decoded_trace.split("</s>")
    code_sentence = sentences[-2]
    print(len(code_sentence.split(" ")))
