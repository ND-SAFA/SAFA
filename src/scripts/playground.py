import os.path

import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, RobertaTokenizer

if __name__ == "__main__":
    tokenizer: RobertaTokenizer = AutoTokenizer.from_pretrained("roberta-base")
    dataset_path = os.path.expanduser("~/desktop/safa/datasets/software-data/drone/originals/definitions")
    issue_path = os.path.join(dataset_path, "designdefinitions.csv")
    issues_df = pd.read_csv(issue_path)
    print("Issues:", len(issues_df))

    code_path = os.path.join(dataset_path, "classes_raw.csv")
    code_df = pd.read_csv(code_path)
    print("Code:", len(code_path))

    MAX_LENGTH = 512
    entries = []
    n_issues = len(issues_df)
    n_code = len(code_df)
    progress_bar = tqdm(total=n_issues * n_code)
    for issue_i in range(n_issues):
        for code_i in range(n_code):
            issue = issues_df.iloc[issue_i]
            issue_id = issue["id"]
            issue_body = issue["content"]
            issue_words = len(issue_body.split(" "))

            code = code_df.iloc[code_i]
            code_id = code["id"]
            code_body = code["text"]
            code_words = len(code_body.split(" "))

            encoded_trace = tokenizer(text=issue_body,
                                      text_pair=code_body,
                                      truncation=True,
                                      max_length=MAX_LENGTH,
                                      padding="max_length",
                                      add_special_tokens=True)
            decoded_trace = tokenizer.decode(encoded_trace["input_ids"])
            sentences = decoded_trace.split("</s>")
            code_sentence = sentences[-2]
            post_code_words = len(code_sentence.split(" "))
            entry = {"s_words": issue_words, "t_words": code_words, "after": post_code_words}
            entries.append(entry)
            progress_bar.update()
    print(pd.DataFrame(entries).mean())
