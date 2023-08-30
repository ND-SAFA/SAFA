import os

from sentence_transformers import SentenceTransformer

CACHE_DIR = os.environ["HF_DATASETS_CACHE"]
CACHED_MODELS = ["sentence-transformers/all-roberta-large-v1",
                 "sentence-transformers/all-MiniLM-L6-v2"]
print("Cache Dir:", CACHE_DIR)
os.makedirs(CACHE_DIR, exist_ok=True)
for m in CACHED_MODELS:
    model = SentenceTransformer(m, cache_folder=CACHE_DIR)
    print(f"{m} has been cached.")
print("All models have been cached.")
