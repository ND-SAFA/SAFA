import gc
import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()
CACHE_DIR = os.environ.get("HF_DATASETS_CACHE", "~/.cache/models")
CACHED_MODELS = ["sentence-transformers/all-MiniLM-L6-v2"]
os.makedirs(CACHE_DIR, exist_ok=True)
print("Cache Dir:", CACHE_DIR)
print("Models:", os.listdir(CACHE_DIR))
os.makedirs(CACHE_DIR, exist_ok=True)
for m in CACHED_MODELS:
    model = SentenceTransformer(m, cache_folder=CACHE_DIR)
    print(f"{m} has been cached.")
print("All models have been cached.")
gc.collect()
