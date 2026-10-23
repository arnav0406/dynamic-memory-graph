"""
Shared configuration for the Dynamic Memory Graph project.

Every module imports its settings from here so values stay consistent:
    from config import MODEL_NAME, GRAPH_PATH
"""

import os

# ---------- Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
GRAPH_PATH = os.path.join(DATA_DIR, "graph.json")
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")
TEST_CONVERSATIONS_PATH = os.path.join(EVAL_DIR, "test_conversations.json")

# ---------- LLM (Ollama) ----------
MODEL_NAME = "llama3.2:3b"
CONTEXT_WINDOW = 2048          # tokens available to the model
LLM_TEMPERATURE = 0.0          # deterministic output for extraction / rewriting
ANSWER_TEMPERATURE = 0.7       # a little variety for final chat answers

# ---------- Extraction ----------
ENTITY_TYPES = ["PERSON", "CONDITION", "DRUG", "PLACE", "PREFERENCE"]
USER_NODE = "User"             # canonical name for the person chatting

# ---------- Query rewriting ----------
HISTORY_TURNS = 4              # recent turns passed to the rewriter

# ---------- Embeddings ----------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# ---------- Graph expansion ----------
MAX_HOPS = 2                   # how far expand() walks from matched entities

# ---------- Retrieval ----------
TOP_K = 5                      # facts injected into the prompt
BM25_TOP_K = 10                # candidates from BM25 before fusion
DENSE_TOP_K = 10               # candidates from FAISS before fusion
GRAPH_TOP_K = 10               # candidates from graph expansion before fusion
RRF_K = 60                     # standard Reciprocal Rank Fusion constant

# ---------- Evaluation ----------
RECALL_K_VALUES = [1, 3, 5]


def ensure_dirs():
    """Create the data folder if it does not exist yet."""
    os.makedirs(DATA_DIR, exist_ok=True)
