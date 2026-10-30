
import numpy as np


def precision_at_k(labels, k=3):
    if not labels:
        return 0.0

    k = min(k, len(labels))
    return round(
        sum(1 for x in labels[:k] if x >= 2) / k,
        3
    )


def recall_at_k(labels, total_relevant, k=3):
    if not labels or total_relevant == 0:
        return 0.0

    k = min(k, len(labels))
    found = sum(1 for x in labels[:k] if x >= 2)

    return round(found / total_relevant, 3)


def ndcg_at_k(labels, k=3):
    if not labels:
        return 0.0

    k = min(k, len(labels))
    actual = np.asarray(labels[:k], dtype=float)

    def dcg(values):
        return sum(
            (2 ** rel - 1) / np.log2(i + 2)
            for i, rel in enumerate(values)
        )

    ideal = sorted(labels, reverse=True)[:k]
    ideal_score = dcg(ideal)

    if ideal_score == 0:
        return 0.0

    return round(float(dcg(actual) / ideal_score), 3)


def evaluate_ranking(ranked_ids, labels, k=3):
    ranked_labels = [labels[x] for x in ranked_ids]

    total_relevant = sum(
        1 for relevance in labels.values()
        if relevance >= 2
    )

    return {
        "Precision@K": precision_at_k(ranked_labels, k),
        "Recall@K": recall_at_k(
            ranked_labels, total_relevant, k
        ),
        "NDCG@K": ndcg_at_k(ranked_labels, k)
    }
