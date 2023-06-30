import os.path

import pandas as pd

from tgen.util.json_util import JsonUtil

if __name__ == "__main__":
    dataset_name = "cm1"
    job_dir = f"~/desktop/safa/experiments/paper/test/{dataset_name}/original/experiment_0/step_0"

    job_dir = os.path.expanduser(job_dir)
    techniques = ["7cb19216-38d3-4344-8604-f44d254e1474",
                  "b336c812-c17f-4f78-a136-f14ceb773987"]


    def read_results(t_name):
        output_path = os.path.join(job_dir, t_name, "output.json")
        return JsonUtil.read_json_file(output_path)["body"]["prediction_entries"]


    t_results = {}
    votes = {}
    correct = {}
    for t in techniques:
        results = read_results(t)

        for entry in results:
            entry_id = f"{entry['source']} - {entry['target']}"
            if entry_id not in votes:
                votes[entry_id] = 0
            if entry["score"] >= 0.5:
                votes[entry_id] += 1
                if entry["label"] == 1:
                    if entry_id not in correct:
                        correct[entry_id] = 0
                    correct[entry_id] += 1

    votes = sorted(votes.items(), key=lambda kv: kv[1], reverse=True)
    votes_df = pd.DataFrame(votes, columns=["trace_id", "count"])

    counts = votes_df["count"].value_counts()
    counts_df = pd.DataFrame(counts)
    count2correct = {count: 0 for count in counts.index}
    for link, correct_count in correct.items():
        for count in counts.index:
            if correct_count >= count:
                count2correct[count] += 1
    counts_df["correct"] = list(count2correct.values())
    print(counts_df.sort_index(ascending=False))
