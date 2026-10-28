"""
Memory manager (owner: Aditya).

Decides what happens to each extracted triple before it goes into the graph.
This version supports:
    ADD  - a new fact is stored as an edge with created_at = timestamp
    SKIP - the exact same fact is already stored, so nothing is added

UPDATE / DELETE and the entity alias dictionary are added on Oct 29.

Usage (from the project root):
    from modules.memory_manager import update_graph
    actions = update_graph(store, triples, "2026-10-28T10:00:00")

Quick test:
    python -m modules.memory_manager
"""

import re

from config import USER_NODE

# Words that refer to the person chatting.
SELF_WORDS = {"i", "me", "my", "myself", "mine", "user", "the user"}


def normalize_entity(name):
    """Clean an entity name: trim spaces and end punctuation, map self-references to USER_NODE."""
    cleaned = " ".join(str(name).split()).strip(" .,!?;:'\"")
    if cleaned.lower() in SELF_WORDS:
        return USER_NODE
    return cleaned


def normalize_predicate(predicate):
    """Clean a predicate into lowercase_with_underscores."""
    cleaned = str(predicate).strip().lower().replace(" ", "_")
    return re.sub(r"[^a-z0-9_]", "", cleaned).strip("_")


def is_duplicate(graph_store, subject, predicate, obj):
    """Return True if this exact fact is already active in the graph."""
    return graph_store.has_edge(subject, predicate, obj, active_only=True)


def update_graph(graph_store, triples, timestamp):
    """Apply ADD / SKIP for each triple and return a list of the actions taken."""
    actions = []
    for triple in triples or []:
        subject = normalize_entity(triple.get("subject", ""))
        predicate = normalize_predicate(triple.get("predicate", ""))
        obj = normalize_entity(triple.get("object", ""))
        object_type = triple.get("object_type")

        if not subject or not predicate or not obj:
            continue

        if is_duplicate(graph_store, subject, predicate, obj):
            op = "SKIP"
        else:
            graph_store.add_edge(subject, predicate, obj, obj_type=object_type, created_at=timestamp)
            op = "ADD"

        actions.append({"op": op, "subject": subject, "predicate": predicate, "object": obj})
    return actions


if __name__ == "__main__":
    import os
    import tempfile

    from modules.graph_store import GraphStore

    store = GraphStore(os.path.join(tempfile.gettempdir(), "dmg_test_memory.json"))
    sample = [
        {"subject": "I", "predicate": "has", "object": "Diabetes", "object_type": "CONDITION"},
        {"subject": "User", "predicate": "takes", "object": "Metformin", "object_type": "DRUG"},
        {"subject": "user", "predicate": "takes", "object": "metformin.", "object_type": "DRUG"},
    ]
    for action in update_graph(store, sample, "2026-10-24T10:00:00"):
        print(action)
    print("Stats:", store.stats())
