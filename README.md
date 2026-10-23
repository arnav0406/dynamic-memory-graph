# Dynamic Memory Graph (DMG)

An external, persistent knowledge graph that gives small LLMs long-term conversational memory.

Small models like **Llama 3.2 3B** have a short context window (2048 tokens), so they forget what a user said a few turns ago. DMG fixes this without fine-tuning. It extracts facts from every user message as structured triples, stores them in a graph, and at query time injects only the relevant facts into the prompt instead of the full chat history.

> Course project, Artificial Intelligence, BML Munjal University.

---

## How it works

```
User message
    │
    ▼
1. Query Rewriter    →  resolves pronouns ("its side effects" → "Metformin side effects")
    │
    ▼
2. Extractor         →  pulls (subject, predicate, object, object_type) triples
    │
    ▼
3. Memory Manager    →  ADD / UPDATE / DELETE facts, links entity aliases, tracks time
    │
    ▼
4. Graph Store       →  NetworkX graph, saved to data/graph.json
    │
    ▼
5. Retriever         →  BM25 + dense search + graph expansion, fused with RRF
    │
    ▼
6. LLM (Ollama)      →  answers using only the retrieved facts
```

**Entity types:** `PERSON`, `CONDITION`, `DRUG`, `PLACE`, `PREFERENCE`

**Example:**

| User says | Stored triple |
|---|---|
| "I'm diabetic and take Metformin" | `(User, has, Diabetes, CONDITION)` |
| | `(User, takes, Metformin, DRUG)` |

Twenty turns later, "What are its side effects?" is rewritten to "What are the side effects of Metformin?", and the stored facts are retrieved and passed to the model.

---

## Tech stack

| Purpose | Tool |
|---|---|
| Language | Python 3.10+ |
| LLM | Ollama, `llama3.2:3b` (runs locally) |
| Graph + persistence | NetworkX (JSON via `node_link_data`) |
| Keyword retrieval | rank-bm25 |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector search | FAISS |
| UI | Streamlit |

---

## Project structure

```
dynamic-memory-graph/
├── README.md
├── requirements.txt
├── config.py                   # shared settings for all modules
├── problem_demo.py             # baseline: Llama failing without memory
├── main.py                     # integration pipeline
├── app.py                      # Streamlit chat UI
│
├── modules/
│   ├── query_rewriter.py       # coreference resolution
│   ├── extractor.py            # entity + triple extraction
│   ├── memory_manager.py       # ADD / UPDATE / DELETE, entity linking
│   ├── graph_store.py          # NetworkX backend, multi-hop expansion, reranking
│   └── retriever.py            # BM25 + RRF hybrid retrieval
│
├── evaluation/
│   ├── eval.py                 # Recall@k + ablation study
│   └── test_conversations.json
│
├── data/                       # graph.json is created here at runtime
└── screenshots/
```

---

## Setup

**1. Install Ollama and pull the model**

Download Ollama from https://ollama.com, then run:

```bash
ollama pull llama3.2:3b
```

**2. Clone the repo and install dependencies**

```bash
git clone https://github.com/<your-username>/dynamic-memory-graph.git
cd dynamic-memory-graph
python -m venv venv
```

Activate the virtual environment:

- Windows: `venv\Scripts\activate`
- macOS / Linux: `source venv/bin/activate`

Then install:

```bash
pip install -r requirements.txt
```

**3. Run**

```bash
streamlit run app.py
```

> The UI and pipeline are under development. Run instructions will be updated as modules land.

---

## Team

| Member | Responsibility |
|---|---|
| Abhishek | Query rewriter (`modules/query_rewriter.py`) |
| Arnav | Entity and triple extractor (`modules/extractor.py`) |
| Aditya | Memory manager (`modules/memory_manager.py`) |
| Arpit | Graph store and reranker (`modules/graph_store.py`) |
| Kartika | Retriever, evaluation, integration, UI, config, docs |

---

## Status

- [x] Project structure and dependencies
- [ ] Extractor
- [ ] Graph store
- [ ] Memory manager
- [ ] Query rewriter
- [ ] Retriever (BM25 → RRF fusion)
- [ ] Integration pipeline
- [ ] Evaluation (Recall@k, ablation)
- [ ] Streamlit UI
