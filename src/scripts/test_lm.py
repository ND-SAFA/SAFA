import os
import sys

from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])

if __name__ == "__main__":
    model_path = "nvidia/nemo-megatron-gpt-5B"
    sentence_a = "The system should have a singleton database connection."
    sentence_b = "The database should be initialized before allowing any endpoints to be served."
    prompt = "A similarity score is a continuous value between 0 and 1 representing how similar two sentences are. What is " \
             f"the similarity score between \"{sentence_a}\" and \"{sentence_b}\""

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    inputs = tokenizer(prompt, return_tensors="pt").input_ids
    model = AutoModelForCausalLM.from_pretrained(model_path)
    outputs = model.generate(inputs, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print("Response: \n", response)
