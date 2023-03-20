import os.path

import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, RobertaTokenizer

from data.processing.cleaning.extract_code_identifiers import ExtractCodeIdentifiersStep
from util.file_util import FileUtil

if __name__ == "__main__":
    tokenizer: RobertaTokenizer = AutoTokenizer.from_pretrained("roberta-base")
    dataset_path = os.path.expanduser("~/desktop/safa/datasets/software-data/drone/originals/definitions")
    source_artifact_path = os.path.join(dataset_path, "designdefinitions.csv")
    source_df = pd.read_csv(source_artifact_path)
    print("Issues:", len(source_df))

    target_data_dir = os.path.join(dataset_path, "flatCode")
    target_artifact_files = list(map(lambda f: {"file": f}, os.listdir(target_data_dir)))
    target_df = pd.DataFrame(target_artifact_files)

    MAX_LENGTH = 512
    entries = []
    n_issues = 20
    n_code = 50
    progress_bar = tqdm(total=n_issues * n_code)
    cleaner = ExtractCodeIdentifiersStep()
    for issue_i in range(n_issues):
        for code_i in range(n_code):
            issue = source_df.sample(n=1).iloc[0]
            issue_id = issue["id"]
            issue_body = issue["content"]
            issue_body = cleaner.run([issue_body])[0]
            issue_words = len(issue_body.split(" "))

            code = target_df.sample(n=1).iloc[0]
            code_body_raw = FileUtil.read_file(os.path.join(target_data_dir, code["file"]))
            code_words = len(code_body_raw.split(" "))

            # code_body = cleaner.run([code_body_raw])[0]
            encoded_trace = tokenizer(text=issue_body,
                                      text_pair=code_body_raw,
                                      truncation=True,
                                      max_length=MAX_LENGTH,
                                      add_special_tokens=True)
            decoded_trace = tokenizer.decode(encoded_trace["input_ids"])
            sentences = decoded_trace.split("</s>")
            code_sentence = sentences[-2]
            post_code_words = len(code_sentence.split(" "))

            entry = {"length": len(encoded_trace["input_ids"]), "t_delta": code_words - post_code_words}
            entries.append(entry)
            progress_bar.update()
    print()
    print(pd.DataFrame(entries).mean())
